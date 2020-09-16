import warnings

from timeseries.base import (
    TimeSeries,
)

from timeseries.errors import (
    NumericValueError,
    OperatorError,
)


class _TimeSeriesOperator:
    """
    Interface class for extending set operations to time series based on dates
    and applying functions to resulting time series.

    :param tseries: time series to operate on
    """
    def __init__(self, tseries):
        """
        Initialize time series operator object.

        :param tseries: time series to operate on
        """
        self.tseries = tseries

    def _apply(self, func, arg, operation, elementwise, fill, **kwargs):
        """
        Apply function to time series after set operation.

        :param func: function to apply to time series
        :param arg: time series or broadcasted argument passed to function
        :param operation: set operation to apply to time series dates
        :param elementwise: flag if function is applied elementwise and should
            return time series
        :param fill: value to fill in missing dates
        :param ``**kwargs``: keyword arguments passed to function
        """
        # apply specified set operation if arg is time series
        if isinstance(arg, TimeSeries):
            dates_set = set(self.tseries.dates)
            dates = self.set_to_dates(getattr(dates_set, operation)(arg.dates))
            # return empty time series if no dates are left after operation
            if len(dates) == 0:
                warnings.warn('time series are empty after set operation')
            # fill out missing dates / contract time series
            if self.tseries.dates != dates or arg.dates != dates:
                # call to constructor leads to some unnecessary overhead - can
                # be further optimized as e.g. input validation can be skipped
                tseries = self._fill_tseries(dates, self.tseries, fill)
                arg = self._fill_tseries(dates, arg, fill)
            else:
                tseries = self.tseries
                arg = arg
        else:
            dates = self.tseries.dates
            tseries = self.tseries
            arg = arg
        # apply function to time series
        try:
            func_value = self._apply_function(tseries, arg, func, elementwise,
                                              **kwargs)
            return func_value
        except Exception:
            raise OperatorError('applying function after set operation failed')

    @classmethod
    def _apply_function(cls, tseries, arg, func, elementwise, **kwargs):
        """
        Apply function to time series and return result, or results as
        timeseries if elementwise.

        :param tseries: time series to operate on
        :param arg: time series or broadcasted argument passed to function
        :param func: function to apply to time series
        :param elementwise: flag if function is applied elementwise and should
            return time series
        :param ``**kwargs``: keyword arguments passed to function
        """
        # skip validation and computation steps if time series is empty
        if len(tseries) == 0:
            values2 = tuple()
        else:
            # attempt to broadcast second argument if not time series
            if not isinstance(arg, TimeSeries):
                values2 = cls._broadcast(arg, len(tseries))
            # check that dates are identical if not broadcasting - should not
            # be possible to raise this unless called outside _apply
            elif tseries.dates != arg.dates:
                raise ValueError('time series dates do not match')
            else:
                values2 = arg.values
        # compute function values
        values1 = tseries.values
        values = func(values1, values2, **kwargs)
        # return time series if function applies elementwise
        if elementwise:
            dates = tseries.dates
            return TimeSeries(dates, values)
        return values

    @staticmethod
    def _broadcast(value, size):
        """
        Return value broadcasted to tuple.

        :param value: float-convertable value
        :param size: size of tuple
        """
        try:
            broadcast_float = float(value)
        except Exception:
            raise NumericValueError(
                'cannot broadcast non-float-convertable value')
        broadcast = tuple(broadcast_float for _ in range(size))
        return broadcast

    @classmethod
    def _fill_tseries(cls, dates, tseries, fill):
        """
        Return time series in specified dates with missing values filled.

        :param tseries: time series object to extend or contract
        :param dates: dates to keep and fill if missing
        :param fill: value to fill in missing dates
        """
        dates_set = set(dates)
        # construct filled values for missing dates
        missing_dates = cls.set_to_dates(dates_set.difference(tseries.dates))
        missing_values = tuple(fill for _ in range(len(missing_dates)))
        # get existing dates and values to keep
        keep_dates = cls.set_to_dates(dates_set.intersection(tseries.dates))
        keep_values = tseries[keep_dates].values
        # concatenate dates and values
        dates = keep_dates + missing_dates
        values = keep_values + missing_values
        return TimeSeries(dates, values)

    @staticmethod
    def set_to_dates(set):
        """
        Convert set of dates to chronologically sorted tuples.
        """
        return tuple(sorted(set))

    def custom(self, func, arg, operation='intersection', elementwise=True,
               fill=0, **kwargs):
        """
        Apply custom function to time series after set operation.

        :param func: function to apply to time series
        :param arg: time series or broadcasted argument passed to function
        :param operation: set operation to apply to time series dates, defaults
            to  'intersection'
        :param elementwise: flag if function is applied elementwise and should
            return time series, defaults to True
        :param fill: value to fill in missing dates, defaults to 0
        :param ``**kwargs``: keyword arguments passed to function
        """
        return self._apply(func, arg, operation, elementwise, fill, **kwargs)


def add(values1, values2):
    """
    Return the element-wise sum of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers
    """
    added_values = tuple(x+y for x, y in zip(values1, values2))
    return added_values


def subtract(values1, values2):
    """
    Return element-wise difference of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers to
        subtract
    """
    differenced_values = tuple(x-y for x, y in zip(values1, values2))
    return differenced_values


def right_subtract(values1, values2):
    """
    Return element-wise right subtraction of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers to
        subtract
    :param values2: finite-length iterable of float-convertable numbers
    """
    return subtract(values2, values1)


def multiply(values1, values2):
    """
    Return element-wise multiplication of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers
    """
    multiplied_values = tuple(x*y for x, y in zip(values1, values2))
    return multiplied_values


def divide(values1, values2):
    """
    Return element-wise division of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers to
        divide with
    """
    divided_values = tuple(x/y for x, y in zip(values1, values2))
    return divided_values


def right_divide(values1, values2):
    """
    Return element-wise right division of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers to
        divide with
    :param values2: finite-length iterable of float-convertable numbers
    """
    return divide(values2, values1)


def power(values1, values2):
    """
    Return element-wise exponentiation of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers to use
        as exponent
    """
    exponentiated_values = tuple(x**y for x, y in zip(values1, values2))
    return exponentiated_values


def right_power(values1, values2):
    """
    Return element-wise right exponentiation of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers to use
        as exponent
    :param values2: finite-length iterable of float-convertable numbers
    """
    return power(values2, values1)
