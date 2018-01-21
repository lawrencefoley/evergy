import json
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s -  - %(message)s", level=logging.INFO)

class KCPL():
    def __init__(self, username, password):
        self.loggedIn = False
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.loginUrl = "https://ala.kcpl.com/ala/login.cfm"
        self.logoutUrl = "https://ala.kcpl.com/ALA/logout.cfm"
        self.selectMeterUrl = "https://ala.kcpl.com/ala/scrDailyUse.cfm"
        self.usageUrl = "https://ala.kcpl.com/ALA/scrDailyUse.cfm"

    def login(self):
        logging.info("Logging in with username: " + self.username)
        loginPayload = {"username": str(self.username), "password": str(self.password)}
        r = self.session.post(url=self.loginUrl, data=loginPayload, allow_redirects=False)
        logging.debug("Response Location header: " + str(r.headers["Location"]))
        if "login" in r.headers["Location"]:
            self.loggedIn = False
            logging.error("Error logging in, was redirect to login page")
        else:
            logging.debug("Login response: " + str(r.status_code))
            self.loggedIn = True

    def logout(self):
        logging.info("Logging out")
        r = self.session.get(url=self.loginUrl)
        self.loggedIn = False

    def getMeters(self):
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

    def getUsage(self, meter):
        if not self.loggedIn:
            logging.error("Must login first")
            return
        meterPayload = {"selectedMeter": str(meter)}
        r = self.session.post(self.usageUrl, meterPayload)

        soup = BeautifulSoup(r.text, 'html.parser')
        data = []
        tables = soup.find_all(id="example")
        if len(tables) < 1:
            logging.debug("Error retrieving data")
            return 
        for row in tables[0].find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 0:
                datum = {}
                datum["date"] = cols[1].text
                datum["reading"] = cols[2].text
                datum["kwh"] = cols[3].text
                datum["cost"] = cols[7].text
                data.append(datum)
        return data

def getCreds():
    with open("../credentials.json", 'r') as f:
        return json.loads(f.read())

if __name__ == "__main__":
    creds = getCreds()
    username = creds["username"]
    password = creds["password"]

    kcpl = KCPL(username, password)
    kcpl.login()
    # Get a list of the meters for your account
    meters = kcpl.getMeters()
    logging.info("Meters: " + str(meters))
    logging.info("Using first meter: " + str(meters[0]))
    # Get readings for a meter
    data = kcpl.getUsage(meters[0])
    logging.info("Last meter reading: " + str(data[0]))
    # End your session by logging out
    kcpl.logout()
