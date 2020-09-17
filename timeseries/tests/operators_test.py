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
        date5 = datetime.fromisoformat('1970-01-05')
        self.dates = (date1, date2, date3)
        self.values = (1, 2, 3)
        self.dates2 = (date1, date2, date4)
        self.values2 = (4, 2, 1)
        self.dates3 = (date3, date1, date5)
        self.values3 = (5, 3, 2)
        self.tseries1 = ts.TimeSeries(self.dates, self.values)
        self.tseries2 = ts.TimeSeries(self.dates2, self.values2)
        self.tseries3 = ts.TimeSeries(self.dates3, self.values3)

    def test_equality(self):
        """
        Test that time series with same dates and values are equal.
        """
        self.assertEqual(
            self.tseries1,
            ts.TimeSeries(self.dates, self.values),
        )

    def test_order_equality(self):
        """
        Test that ordering of dates and values does not affect equality.
        """
        self.assertEqual(
            self.tseries1,
            ts.TimeSeries(self.dates[::-1], self.values[::-1]),
        )

    def test_dates_nonequality(self):
        """
        Test that time series with different dates are not equal.
        """
        self.assertNotEqual(
            self.tseries1,
            ts.TimeSeries(self.dates2, self.values),
        )

    def test_values_nonequality(self):
        """
        Test that time series with different values are not equal.
        """
        self.assertNotEqual(
            self.tseries1,
            ts.TimeSeries(self.dates, self.values2),
        )

    def test_custom_sum(self):
        """
        Test that time series values can be summed with custom operator.
        """
        def sum_func(values1, values2):
            return sum((x+y for x, y in zip(values1, values2)))
        self.assertEqual(
            self.tseries1.operator.custom(sum_func, 0, elementwise=False),
            sum(self.tseries1.values),
        )

    def test_broadcasting(self):
        """
        Test that time series values are broadcasted properly.
        """
        def broadcast_func(x): return 2**x + x/2 + 5 - x
        self.assertEqual(
            broadcast_func(self.tseries1).values,
            tuple(broadcast_func(x) for x in self.values),
        )

    def test_sign_reversal(self):
        """
        Test that time series multiplication by -1 reverses signs.
        """
        self.assertEqual(
            self.tseries1 - self.tseries2,
            (self.tseries2 - self.tseries1) * -1,
        )

    def test_commutative_addition(self):
        """
        Test that time series addition is commutative.
        """
        self.assertEqual(
            self.tseries1 + self.tseries2,
            self.tseries2 + self.tseries1,
        )

    def test_commutative_multiplication(self):
        """
        Test that time series multiplication is commutative.
        """
        self.assertEqual(
            self.tseries1 * self.tseries2,
            self.tseries2 * self.tseries1,
        )

    def test_noncommutative_subtraction(self):
        """
        Test that time series subtraction is not commutative.
        """
        # can be equal, watch out if changing test values
        self.assertNotEqual(
            self.tseries1 - self.tseries2,
            self.tseries2 - self.tseries1,
        )

    def test_noncommutative_division(self):
        """
        Test that time series division is not commutative.
        """
        # can be equal, watch out if changing test values
        self.assertNotEqual(
            self.tseries1 / self.tseries2,
            self.tseries2 / self.tseries1,
        )

    def test_associativity_addition(self):
        """
        Test that time series addition is associative.
        """
        self.assertEqual(
            (self.tseries1 + self.tseries2) + self.tseries3,
            self.tseries1 + (self.tseries2 + self.tseries3),
        )

    def test_associativity_multiplication(self):
        """
        Test that time series multiplication is associative.
        """
        self.assertEqual(
            (self.tseries1 * self.tseries2) * self.tseries3,
            self.tseries1 * (self.tseries2 * self.tseries3),
        )

    def test_nonassociativity_subtraction(self):
        """
        Test that time series subtraction is not associative.
        """
        # can be equal, watch out if changing test values
        self.assertNotEqual(
            (self.tseries1 - self.tseries2) - self.tseries3,
            self.tseries1 - (self.tseries2 - self.tseries3),
        )

    def test_nonassociativity_division(self):
        """
        Test that time series division is not associative.
        """
        # can be equal, watch out if changing test values
        self.assertNotEqual(
            (self.tseries1 / self.tseries2) / self.tseries3,
            self.tseries1 / (self.tseries2 / self.tseries3),
        )

    def test_distributivity_multiplication(self):
        """
        Test that time series multiplication is distributive.
        """
        self.assertEqual(
            self.tseries1*(self.tseries2 + self.tseries3),
            self.tseries1*self.tseries2 + self.tseries1*self.tseries3,
        )

    def test_nondistributivity_division(self):
        """
        Test that time series division is not distributive.
        """
        self.assertNotEqual(
            self.tseries1/(self.tseries2 + self.tseries3),
            self.tseries1/self.tseries2 + self.tseries1/self.tseries3,
        )
