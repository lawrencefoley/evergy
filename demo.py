import json

from evergy.evergy import Evergy


def get_creds():
    with open("credentials.json", "r") as f:
        return json.loads(f.read())


creds = get_creds()
username = creds["username"]
password = creds["password"]

evergy = Evergy(username, password)

data = evergy.get_usage()
print("Today's kWh: " + str(data[-1]["usage"]))
