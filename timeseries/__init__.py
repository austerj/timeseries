__docformat__ = 'restructuredtext'
__all__ = (
    'TimeSeries',
    'read_csv',
    'samples_path',
)

import os
import sys
import warnings

# warning if importing with Python pre-3.7
if sys.version_info < (3, 7):
    warnings.warn(
        'package assumes insertion ordered \'dict\' introduced in Python 3.7',
        RuntimeWarning,
        stacklevel=2,
    )

# components to include on import
import timeseries.filter
import timeseries.stats
import timeseries.operator

from timeseries.base import (
    TimeSeries,
)

from timeseries.io import (
    read_csv,
)

# define path to package and sample data
package_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
samples_path = os.path.join(package_path, 'samples', '')


# load all relevant tests during unittest discovery
def load_tests(loader, tests, ignore):
    # modules containing doctests
    import doctest
    import timeseries as ts
    doctest_modules = (
        ts.base,
        ts.io,
        ts.filter.weights,
        ts.stats,
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
