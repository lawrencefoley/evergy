import json
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s -  - %(message)s", level=logging.INFO)

day_before_yesterday = date.today() - timedelta(days=2)
yesterday = date.today() - timedelta(days=1)
today = date.today()

class KCPL():
    def __init__(self, username, password):
        self.loggedIn = False
        self.session = None
        self.username = username
        self.password = password
        self.accountNumber = None
        self.premiseId = None
        self.loginUrl = "https://www.evergy.com/log-in"
        self.logoutUrl = "https://www.evergy.com/logout"
        self.accountSummaryUrl = "https://www.evergy.com/ma/my-account/account-summary"
        self.accountDashboardUrl = "https://www.evergy.com/api/account/{accountNum}/dashboard/current"
        self.usageDataUrl = "https://www.evergy.com/api/report/usage/{premiseId}?interval={query_scale}&from={start}&to={end}"

    def login(self):
        self.session = requests.Session()
        logging.info("Logging in with username: " + self.username)
        loginPayload = {"username": str(self.username), "password": str(self.password)}
        r = self.session.post(url=self.loginUrl, data=loginPayload, allow_redirects=False)
        logging.debug("Login response: " + str(r.status_code))
        r = self.session.get(self.accountSummaryUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        accountData = soup.find_all('script', id='account-landing-data')
        if len(accountData) == 0:
            self.loggedIn = False
        else:
            self.accountNumber = json.loads(accountData[0].contents[0])["accountNumber"]
            dashboardData = self.session.get(self.accountDashboardUrl.format(accountNum=self.accountNumber)).json()
            self.premiseId = dashboardData["addresses"][0]["premiseId"]
            self.loggedIn = self.accountNumber is not None and self.premiseId is not None

    def logout(self):
        logging.info("Logging out")
        self.session.get(url=self.logoutUrl)
        self.session = None
        self.loggedIn = False


    def getUsage(self, start=day_before_yesterday, end=yesterday, query_scale="d"):
        """Fetches all usage data from the given period."""
        if not self.loggedIn:
            logging.error("Must login first")
            return
        url = self.usageDataUrl.format(premiseId=self.premiseId, query_scale=query_scale, start=start, end=end)
        logging.debug("fetching {}".format(url))
        usageData = self.session.get(url).json()
        return usageData["data"]

def getCreds():
    with open("../credentials.json", 'r') as f:
        return json.loads(f.read())

if __name__ == "__main__":
    # Read the credentials.json file
    creds = getCreds()
    username = creds["username"]
    password = creds["password"]

    kcpl = KCPL(username, password)
    kcpl.login()

    # Get a list of daily readings

    data = kcpl.getUsage()
    logging.info("Last usage data: " + str(data[-1]))
    logging.info("Last usage reading: " + str(data[-1]["usage"]))

    # End your session by logging out
    kcpl.logout()
