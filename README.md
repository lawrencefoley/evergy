# ⚡Evergy Client
[![Latest Version on PyPi](https://badge.fury.io/py/evergy.svg)](https://pypi.org/project/evergy/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/evergy.svg)](https://pypi.org/project/evergy/)
[![Documentation Status](https://readthedocs.org/projects/evergy/badge/?version=latest)](https://evergy.readthedocs.io/en/latest/)
[![Requriements Status](https://requires.io/github/lawrencefoley/evergy/requirements.svg?branch=master)](https://requires.io/github/lawrencefoley/evergy/requirements/?branch=master)

A simple utility that you can use to login to your Evergy account and retrieve you meter readings.
- **[Documentation](https://evergy.readthedocs.io/en/latest/)**
- **[Source Code](https://github.com/lawrencefoley/evergy)**
> **Note: This is an unofficial utility that uses Evergy's non-public API.**

> Previously known as "KCPL"

## Install
```
pip install evergy
```

## Usage
```python
from evergy.evergy import Evergy

evergy = Evergy("<evergy-username>", "<evergy-password>")

data = evergy.get_usage()
print("Today's kWh: " + str(data[-1]["usage"]))
```

### Output
The last element from the `get_usage()` will be the latest data. The `usage` is in kilowatt-hours. I believe the `peakDateTime` is the
time during that day when your usage was the highest and the `peakDemand` is how many kilowatts you were drawing at that time.
```text
Latest data:
{
    'period': 'Saturday',
    'billStart': '0001-01-01T00:00:00',
    'billEnd': '0001-01-01T00:00:00',
    'billDate': '2021-09-18T00:00:00',
    'date': '9/18/2021',
    'usage': 14.7756,
    'demand': 3.7992,
    'avgDemand': 0.0,
    'peakDemand': 3.7992,
    'peakDateTime': '12:45 p.m.',
    'maxTemp': 71.0,
    'minTemp': 71.0,
    'avgTemp': 71.0,
    'cost': 18.5748, 
    'isPartial': False
}
```
## Related Projects
- [KC Water](https://github.com/patrickjmcd/kcwater): A similar project developed by [Patrick McDonagh](https://github.com/patrickjmcd). Check it out!

## Development
### Setup
```powershell
python -m pip install --upgrade virtualenv
virtualenv venv
.\venv\Scripts\activate.ps1
```

### Code Formatting
Install the dev dependencies and run `isort` and `flake8` to properly format the code.
```bash
pip install -r requirements_dev.txt
isort evergy/
flake8 evergy/
```

### Build Docs
Windows PowerShell:
```powershell
pip install -r docs/requirements_docs.txt
docs\make.bat clean; docs\make.bat html
```

### Release New Version
- Bump `__version__` in `evergy/__init__.py` 
```bash
git commit -m "Bump version"
git tag -a v1.0.1 -m "v1.0.1"
git push --tags
```

### Build Wheel
> The `--no-isolation` flag tells it to use the existing virtual env
```bash
python -m build --no-isolation --wheel
```

### Upload to PyPi
#### Test
```bash
twine upload --verbose --repository testpypi dist/*
```

#### Prod
```bash
twine upload --verbose --repository pypi dist/*
```
