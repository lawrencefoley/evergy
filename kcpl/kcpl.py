import json
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s -  - %(message)s", level=logging.INFO)

class KCPL():
    def __init__(self, username, password):
        self.loggedIn = False
        self.session = None
        self.username = username
        self.password = password
        self.accountNumber = None
        self.premiseId = None
        self.loginUrl = "https://www.kcpl.com/log-in"
        self.logoutUrl = "https://www.kcpl.com/logout"
        self.accountSummaryPageUrl = "https://www.kcpl.com/ma/my-account/account-summary/single-account"
        self.accountDashboardUrl = "https://www.kcpl.com/api/account/{accountNum}/dashboard/current"
        self.reportUrl = "https://www.kcpl.com/api/account/{accountNum}/dashboard/{year}{monthTwoDigit}/report"

    def login(self):
        self.session = requests.Session()
        logging.info("Logging in with username: " + self.username)
        loginPayload = {"Username": str(self.username), "Password": str(self.password)}
        r = self.session.post(url=self.loginUrl, data=loginPayload, allow_redirects=False)
        logging.debug("Login response: " + str(r.status_code))
        r = self.session.get(self.accountSummaryPageUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        accountData = soup.find_all('script', id='account-landing-data')
        if len(accountData) == 0:
            self.loggedIn = False
        else:
            self.accountNumber = json.loads(accountData[0].text)["accountNumber"]
            dashBoardData = self.session.get(self.accountDashboardUrl.replace("{accountNum}", self.accountNumber)).json()
            self.premiseId = dashBoardData["addresses"][0]["premiseId"]
            self.loggedIn = self.accountNumber is not None and self.premiseId is not None

    def logout(self):
        logging.info("Logging out")
        r = self.session.get(url=self.logoutUrl)
        self.session = None
        self.loggedIn = False

    def getMeters(self):
        logging.warn("getMeters() has been deprecated! KCPL removed meters from their website and API and now just rolls all meters up into a total")
        if not self.loggedIn:
            logging.error("Must login first")
            return
        meters = []
        r = self.session.get(self.selectMeterUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        picklist = soup.find_all("select", {"name":"selectedMeter"})
        if len(picklist) == 0:
            logging.debug("Could not find meter list")
            return meters
        else:
            picklistItems = picklist[0].find_all("option")
            for item in picklistItems:
                meters.append(item.text)
            return meters

    def getUsage(self):
        if not self.loggedIn:
            logging.error("Must login first")
            return
        # TODO Allow querying for month instead of day
        usageData = self.session.get("https://www.kcpl.com/api/report/usage/" + self.premiseId + "?interval=d").json()
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
