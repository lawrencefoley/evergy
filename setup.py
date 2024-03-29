# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import find_packages, setup
import evergy
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="UTF-8") as f:
    long_description = f.read()

setup(
    name="evergy",
    version=evergy.__version__,
    description="A utility that reads electric utility meter data from Evergy.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/lawrencefoley/evergy",
    project_urls={
        'Documentation': 'https://evergy.readthedocs.io/en/latest/',
        'Source': 'https://github.com/lawrencefoley/evergy/',
        'Tracker': 'https://github.com/lawrencefoley/evergy/issues',
        'Maintainer': 'https://lawrencefoley.com',
    },
    author="Lawrence Foley",
    author_email="lawrencefoley@live.com",
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="evergy kcpl kansas-city electricity-consumption electricity-meter api",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=[]),  # Required
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["beautifulsoup4==4.10.0", "requests==2.26.0"],  # Optional
    python_requires='>=3',
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    package_data={  # Optional
        "credentials": ["credentials.json"],
        "README": ["README.md"],
    },
)
