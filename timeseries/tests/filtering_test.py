from unittest import TestCase
from datetime import datetime

import timeseries as ts


class TestCustomFiltering(TestCase):
    """
    Test that custom filtering functions can replicate built-in methods.
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
        self.window_size = 2
        self.alpha = 0.1

    def test_moving_average(self):
        """
        Test that moving average can be replicated.
        """
        def sum_func(x): return sum(x)
        self.assertEqual(
            self.tseries.moving_average(self.window_size),
            self.tseries.rolling(self.window_size).custom(sum_func),
        )

    def test_exponential_moving_average(self):
        """
        Test that exponential moving average can be replicated.
        """
        alpha = 0.2
        def identity(x): return x
        self.assertEqual(
            self.tseries.exponential_moving_average(alpha),
            (self.tseries.rolling(weights='none')
                         .exponential_custom(identity, alpha)),
        )

    def test_identity(self):
        """
        Test that exponential moving average without smoothing returns original
        time series.
        """
        alpha = 1
        def identity(x): return x
        self.assertEqual(
            self.tseries.exponential_moving_average(alpha),
            (self.tseries.rolling(weights='none')
                         .exponential_custom(identity, alpha)),
        )
