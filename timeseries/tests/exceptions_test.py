from unittest import TestCase
from datetime import datetime
from itertools import count

import timeseries as ts
from timeseries.errors import (
        DateError,
        NumericValueError,
        InputDimensionError,
        IteratorError,
        CSVLoadError,
        CSVDateError,
        WeightsError,
)


class TestTimeSeriesExceptionHandling(TestCase):
    """
    Test that core TimeSeries methods raise expected exceptions.
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

    def test_nolen_input(self):
        """
        Test that non-terminating generator inputs raise IteratorError.
        """
        self.assertRaises(
            IteratorError,
            ts.TimeSeries,
            count(),
            count(),
        )

    def test_dimension_mismatch_input(self):
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


class TestCSVExceptionHandling(TestCase):
    """
    Test that CSV functions and methods raise expected exceptions.
    """
    def test_nonfloat_offset(self):
        """
        Test that non-float offset from UNIX epoch raises CSVLoadError.
        """
        self.assertRaises(
            CSVLoadError,
            ts.read_csv,
            ts.samples_path + 'iso.csv',
        )

    def test_dateformat_mismatch(self):
        """
        Test that using a mismatched data format raises CSVLoadError.
        """
        mismatch_format = '%Y-%m-%d'
        self.assertRaises(
            CSVLoadError,
            ts.read_csv,
            ts.samples_path + 'epoch.csv',
            to_datetime=mismatch_format,
        )

    def test_noncallable_nonstr_dateformat(self):
        """
        Test that non-callable non-str date format raises CSVDateError.
        """
        invalid_format = 42
        self.assertRaises(
            CSVDateError,
            ts.read_csv,
            ts.samples_path + 'epoch.csv',
            to_datetime=invalid_format,
        )

    def test_column_mismatch(self):
        """
        Test that mismatched column name raises CSVLoadError.
        """
        mismatch_date_column = 'not_times'
        self.assertRaises(
            CSVLoadError,
            ts.read_csv,
            ts.samples_path + 'epoch.csv',
            date_column=mismatch_date_column,
        )


class TestFilteringExceptionHandling(TestCase):
    """
    Test that filtering raises expected exceptions.
    """
    def test_negative_min_weight(self):
        """
        Test that minimum weight below 0 in LinearWeights raises WeightsError.
        """
        negative_min_weight = -0.1
        self.assertRaises(
            WeightsError,
            ts.filter.weights.LinearWeights,
            negative_min_weight,
        )

    def test_greater_than_one_min_weight(self):
        """
        Test that minimum weight above 1 in LinearWeights raises WeightsError.
        """
        greater_than_one_min_weight = 1.1
        self.assertRaises(
            WeightsError,
            ts.filter.weights.LinearWeights,
            greater_than_one_min_weight,
        )
