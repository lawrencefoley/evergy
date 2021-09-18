# ⚡Evergy Client
A simple utility that you can use to login to your Evergy account and retrieve you meter readings.
> **Note: This is an unofficial utility that uses Evergy's non-public API.**

> Previously known as "KCPL"

## Install
```
pip install --upgrade git+git://github.com/lawrencefoley/evergy.git
```

## Usage

```python
# Import the package
from evergy import Evergy

# Login
evergy = Evergy("username", "password")
evergy.login()

# Get a list of daily readings
# Note, there is more data available such as 'cost' and 'avgTemp'
data = evergy.get_usage()
logging.info("Last usage reading: " + str(data[-1]))
logging.info("Last usage reading: " + str(data[-1]["usage"]))

# End your session by logging out
evergy.logout()
```

## Development
### Code Formatting
Install the dev dependencies and run `isort` and `flake8` to properly format the code.
```bash
pip install -r requirements_dev.txt
isort evergy/
flake8 evergy/
```

### Release New Version
```bash
git commit -m "Bump version"
git tag -a v1.0.1 -m "v1.0.1"
git push --tags
```

### Build Docs
Windows PowerShell:
```powershell
.\make.bat clean; .\make.bat html
```
