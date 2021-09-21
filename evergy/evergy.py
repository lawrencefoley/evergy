import json
import logging
from datetime import date
from typing import Final

from .utils import get_past_date

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)

DAY_INTERVAL: Final = "d"
HOUR_INTERVAL: Final = "h"
FIFTEEN_MINUTE_INTERVAL: Final = "mi"

day_before_yesterday = get_past_date(2)
yesterday = get_past_date(1)
today = date.today()


class Evergy:
    def __init__(self, username, password):
        self.logged_in = False
        self.session = None
        self.username = username
        self.password = password
        self.account_number = None
        self.premise_id = None
        self.login_url = "https://www.evergy.com/log-in"
        self.logout_url = "https://www.evergy.com/logout"
        self.account_summary_url = (
            "https://www.evergy.com/ma/my-account/account-summary"
        )
        self.account_dashboard_url = (
            "https://www.evergy.com/api/account/{accountNum}/dashboard/current"
        )
        self.usageDataUrl = "https://www.evergy.com/api/report/usage/{premise_id}?interval={interval}&from={start}&to={end}"

    def login(self):
        self.session = requests.Session()
        logging.info("Logging in with username: " + self.username)
        login_form = self.session.get(self.login_url)
        login_form_soup = BeautifulSoup(login_form.text, "html.parser")
        csrf_token = login_form_soup.select(".login-form > input")[0]["value"]
        csrf_token_name = login_form_soup.select(".login-form > input")[0]["name"]
        login_payload = {
            "Username": str(self.username),
            "Password": str(self.password),
            csrf_token_name: csrf_token,
        }
        r = self.session.post(
            url=self.login_url, data=login_payload, allow_redirects=False
        )
        logging.debug("Login response: " + str(r.status_code))
        r = self.session.get(self.account_summary_url)
        soup = BeautifulSoup(r.text, "html.parser")
        account_data = soup.find_all("script", id="account-landing-data")
        if len(account_data) == 0:
            self.logged_in = False
        else:
            self.account_number = json.loads(account_data[0].contents[0])[
                "accountNumber"
            ]
            dashboard_data = self.session.get(
                self.account_dashboard_url.format(accountNum=self.account_number)
            ).json()
            self.premise_id = dashboard_data["addresses"][0]["premiseId"]
            self.logged_in = (
                self.account_number is not None and self.premise_id is not None
            )

    def logout(self):
        logging.info("Logging out")
        self.session.get(url=self.logout_url)
        self.session = None
        self.logged_in = False

    def get_usage(self, days: int = 1, interval: str = DAY_INTERVAL) -> [dict]:
        """
        Gets the energy usage for previous days up until today. Useful for getting the most recent data.
        :rtype: [dict]
        :param days: The number of back to get data for.
        :param interval: The time period between each data element in the returned data. Default is days.
        :return: A list of usage elements. The number of elements will depend on the `interval` argument.
        """
        return self.get_usage_range(get_past_date(days_back=days), get_past_date(0), interval=interval)

    def get_usage_range(self, start: date = get_past_date(0), end: date = get_past_date(0), interval: str = DAY_INTERVAL) -> [dict]:
        """
        Gets a specific range of historical usage. Could be useful for reporting.
        :param start: The date to begin getting data for (inclusive)
        :param end: The last date to get data for (inclusive)
        :param interval: The time period between each data element in the returned data. Default is days.
        :return: A list of usage elements. The number of elements will depend on the `interval` argument.
        """
        if not self.logged_in:
            self.login()
        url = self.usageDataUrl.format(
            premise_id=self.premise_id, interval=interval, start=start, end=end
        )
        logging.info("Fetching {}".format(url))
        usage_response = self.session.get(url)
        # A 403 is return if the user got logged out from inactivity
        if usage_response.status_code == 403:
            logging.info("Received HTTP 403, logging in again")
            self.login()
            usage_response = self.session.get(url)
        return usage_response.json()["data"]


def get_creds():
    with open("../credentials.json", "r") as f:
        return json.loads(f.read())


if __name__ == "__main__":
    creds = get_creds()
    username = creds["username"]
    password = creds["password"]

    evergy = Evergy(username, password)

    data = evergy.get_usage()
    logging.info("Today's kWh: " + str(data[-1]["usage"]))
