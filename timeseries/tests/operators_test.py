from unittest import TestCase
from datetime import datetime
import timeseries as ts


class TestTimeSeriesOperators(TestCase):
    """
    Test that TimeSeries operators work as expected.
    """
    def setUp(self):
        """
        Initialize values for test cases.
        """
        date1 = datetime.fromisoformat('1970-01-01')
        date2 = datetime.fromisoformat('1970-01-02')
        date3 = datetime.fromisoformat('1970-01-03')
        date4 = datetime.fromisoformat('1970-01-04')
        self.dates = (date1, date2, date3)
        self.values = (1, 2, 3)
        self.other_dates = (date1, date2, date4)
        self.other_values = (1, 2, 4)
        self.tseries = ts.TimeSeries(self.dates, self.values)

    def test_equality(self):
        """
        Test that time series with same dates and values are equal.
        """
        self.assertEqual(
            self.tseries,
            ts.TimeSeries(self.dates, self.values),
        )

    def test_order_equality(self):
        """
        Test that ordering of dates and values does not affect equality.
        """
        self.assertEqual(
            self.tseries,
            ts.TimeSeries(self.dates[::-1], self.values[::-1]),
        )

    def test_dates_nonequality(self):
        """
        Test that time series with different dates are not equal.
        """
        self.assertNotEqual(
            self.tseries,
            ts.TimeSeries(self.other_dates, self.values),
        )

    def test_values_nonequality(self):
        """
        Test that time series with different values are not equal.
        """
        self.assertNotEqual(
            self.tseries,
            ts.TimeSeries(self.dates, self.other_values),
        )
