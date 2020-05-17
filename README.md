## Meter Data Utility for Evergy (previously known as Kansas City Power and Light)
A simple utility that you can use to login to your Evergy account and retrieve you meter readings.

## Install
```
pip install git+git://github.com/lawrencefoley/kcpl.git
```

## Usage
```python
# Import the package
from kcpl.kcpl import KCPL

# Login
kcpl = KCPL("username", "password")
kcpl.login()

# Get a list of daily readings
# Note, there is more data available such as 'cost' and 'avgTemp'
data = kcpl.getUsage()
logging.info("Last usage reading: " + str(data[-1]))
logging.info("Last usage reading: " + str(data[-1]["usage"]))

# End your session by logging out
kcpl.logout()
```
