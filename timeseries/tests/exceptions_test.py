import unittest
from datetime import datetime
from itertools import count

import timeseries as ts
from timeseries.errors import (
        DateError,
        NumericValueError,
        InputDimensionError,
        IteratorError,
)


class TestExceptionHandling(unittest.TestCase):
    """
    Test that TimeSeries methods raise expected exceptions.
    """
    def setUp(self):
        """
        Initialize values for test cases.
        """
        date1 = datetime.fromisoformat('1970-01-01')
        date2 = datetime.fromisoformat('1970-01-02')
        date3 = datetime.fromisoformat('1970-01-03')
        self.dates = (date1, date2, date3)
        self.values = (1, 2, 3)
        self.tseries = ts.TimeSeries(self.dates, self.values)

    def test_noniterable_input(self):
        """
        Test that non-iterable inputs raise IteratorError.
        """
        self.assertRaises(
            IteratorError,
            ts.TimeSeries,
            self.dates[0],
            self.values[0],
        )

    def test_nonlen_input(self):
        """
        Test that non-terminating generator inputs raise IteratorError.
        """
        self.assertRaises(
            IteratorError,
            ts.TimeSeries,
            count(),
            count(),
        )

    def test_dimensionmismatch_input(self):
        """
        Test that dimension-mismatched inputs raise InputDimensionError.
        """
        self.assertRaises(
            InputDimensionError,
            ts.TimeSeries,
            self.dates[0:2],
            self.values,
        )

    def test_nondatetime_input(self):
        """
        Test that non-datetime date inputs raise DateError.
        """
        self.assertRaises(
            DateError,
            ts.TimeSeries,
            self.values,
            self.values,
        )

    def test_nonfloat_input(self):
        """
        Test that non-float-convertable value inputs raise NumericValueError.
        """
        self.assertRaises(
            NumericValueError,
            ts.TimeSeries,
            self.dates,
            ('a', 'b', 'c'),
        )

    def test_noentry_get_value(self):
        """
        Test that missing entry on get_value raises KeyError.
        """
        missing_date = datetime.fromisoformat('1970-01-04')
        self.assertRaises(
            KeyError,
            self.tseries.get_value,
            missing_date,
        )

    def test_noniso_get_value(self):
        """
        Test that invalid ISO date string for get_value raises DateError.
        """
        invalid_iso = '01.01.1970'
        self.assertRaises(
            DateError,
            self.tseries.get_value,
            invalid_iso,
        )
