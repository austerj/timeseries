__docformat__ = 'restructuredtext'
__all__ = (
    'TimeSeries',
    'read_csv',
    'samples',
)

import os

# submodules to include on import
from timeseries.base import (
    TimeSeries,
)

from timeseries.io import (
    read_csv,
)

# define path to sample data
package_path = os.path.join(os.getcwd(), 'timeseries')
samples = os.path.join(package_path, 'samples', '')

# load all relevant tests during unittest discovery
def load_tests(loader, tests, ignore):
    # submodules containing doctests
    import doctest
    import timeseries as ts
    doctest_modules = (
        ts.base,
        ts.io,
    )
    # doctests are used to test basic functionality with valid inputs
    for submodule in doctest_modules:
        tests.addTest(doctest.DocTestSuite(submodule))
    # unit tests are used to test exception handling and complex functionality
    unittests = loader.discover(
        start_dir='./timeseries/tests',
        pattern='*_test.py'
    )
    tests.addTests(unittests)
    return tests
