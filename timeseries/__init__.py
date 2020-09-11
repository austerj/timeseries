__docformat__ = 'restructuredtext'

import warnings

# submodules to include on import
from timeseries.base import (
	TimeSeries,
)

# submodules containing doctests
import timeseries as ts
doctest_modules = (
        ts.base,
)

# include doctests in unittest discovery
def load_tests(loader, tests, ignore):
    import doctest
    for submodule in doctest_modules:
        tests.addTest(doctest.DocTestSuite(submodule))
    return tests
