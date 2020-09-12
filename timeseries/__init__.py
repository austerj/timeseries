__docformat__ = 'restructuredtext'

# submodules to include on import
from timeseries.base import (
    TimeSeries,
)
__all__ = (
    'TimeSeries',
)


# load all relevant tests during unittest discovery
def load_tests(loader, tests, ignore):
    # submodules containing doctests
    import doctest
    import timeseries as ts
    doctest_modules = (
        ts.base,
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
