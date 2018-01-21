## Meter Data Utility for Kansas City Power and Light
A simple utility that you can use to login to your KCPL account and retrieve you meter readings.

## Install
```
pip install git+git://github.com/lawrencefoley/kcpl.git
```

## Usage
```python
# Import the package
from kcpl.kcpl import KCPL
kcpl = KCPL("username", "password")
kcpl.login()
# Get a list of the meters for your account
meters = kcpl.getMeters()
print("Meters: " + str(meters))
print("Using first meter: " + str(meters[0]))
# Get readings for a meter
data = kcpl.getUsage(meters[0])
print("Last meter reading: " + str(data[0]))
# End your session by logging out
kcpl.logout()
```
