# timeseries

### Overview
**timeseries** is a Python package that provides a one-dimensional time series data structure built entirely from the [Python Standard Library](https://docs.python.org/3/library/index.html). Time series objects can be instantiated from CSV files and provide basic computational capabilities, including sample statistics, overloaded arithmetic operations and filtering (rolling windows, exponential moving averages etc.).

### Documentation
The latest build of the documentation is available on [GitHub Pages](https://austerj.github.io/timeseries/). Documentation is generated with [sphinx](https://www.sphinx-doc.org/en/master/) using the [Read the Docs](https://sphinx-rtd-theme.readthedocs.io/en/stable/) theme.

### Installation
Python **version 3.7 at minimum** is required for the package, since the logic depends on ordering of dictionaries and [datetime](https://docs.python.org/3/library/datetime.html) functionality introduced in version 3.7. There are no third-party module dependencies. The package can be installed directly with the command
```sh
$ pip3 install git+https://github.com/austerj/timeseries
```
Alternatively the package can be cloned and installed locally in editable mode with
```sh
$ git clone https://github.com/austerj/timeseries
$ pip3 install -e ./timeseries
```
or even imported directly from the REPL in the parent directory with
```py
import timeseries as ts
```

### Running unit tests
The package uses the [doctest](https://docs.python.org/3/library/doctest.html) and [unittest](https://docs.python.org/3/library/unittest.html) modules from the [Python Standard Library](https://docs.python.org/3/library/index.html) for testing. All tests can be executed by running the command
```sh
$ python3 -m unittest -v
```
in the parent directory of the cloned repository.
