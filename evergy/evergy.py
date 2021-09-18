import json
import logging
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -  - %(message)s", level=logging.INFO
)

day_before_yesterday = date.today() - timedelta(days=2)
yesterday = date.today() - timedelta(days=1)
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
        self.usageDataUrl = "https://www.evergy.com/api/report/usage/{premise_id}?interval={query_scale}&from={start}&to={end}"

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

    def get_usage(self, start=day_before_yesterday, end=yesterday, query_scale="d"):
        """Fetches all usage data from the given period."""
        if not self.logged_in:
            logging.error("Must login first")
            return
        url = self.usageDataUrl.format(
            premise_id=self.premise_id, query_scale=query_scale, start=start, end=end
        )
        logging.debug("fetching {}".format(url))
        usage_data = self.session.get(url).json()
        return usage_data["data"]


def get_creds():
    with open("../credentials.json", "r") as f:
        return json.loads(f.read())


if __name__ == "__main__":
    # Read the credentials.json file
    creds = get_creds()
    username = creds["username"]
    password = creds["password"]

    evergy = Evergy(username, password)
    evergy.login()

    # Get a list of daily readings
    data = evergy.get_usage()
    logging.info("Last usage data: " + str(data[-1]))
    logging.info("Last usage reading: " + str(data[-1]["usage"]))

    # End your session by logging out
    evergy.logout()
