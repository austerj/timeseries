import warnings
from datetime import datetime

from timeseries.errors import (
    DateError,
    NumericValueError,
    InputDimensionError,
    IteratorError,
)


class TimeSeries:
    """
    Data structure for one-dimensional time series.

    Allows for easy indexing and various convenient time series calculations
    including mean, variance, customizable filtering, cross-correlations,
    element-wise addition etc. Time series data is automatically sorted in
    chronological order by date.

    :param dates: finite-length iterable of datetime objects
    :param values: finite-length iterable of float-convertable numbers

    :example:

    >>> from datetime import datetime
    >>> import timeseries as ts
    >>> date1 = datetime.fromisoformat('1970-01-01')
    >>> date2 = datetime.fromisoformat('1970-01-02')
    >>> date3 = datetime.fromisoformat('1970-01-03')
    >>> dates = (date2, date1, date3)
    >>> values = (2, 1, 3)
    >>> tseries = ts.TimeSeries(dates, values)

    The time series is automatically ordered by dates with the earliest entry
    on top and the latest entry at the bottom. Various attributes allow for
    inspection of the data contained in the time series.

    >>> tseries
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00

    >>> tseries.dates[1]
    datetime.datetime(1970, 1, 2, 0, 0)

    >>> tseries.iso_dates
    ('1970-01-01T00:00:00', '1970-01-02T00:00:00', '1970-01-03T00:00:00')

    >>> tseries.values
    (1.0, 2.0, 3.0)

    The get_value method can be called explicitly to retrieve the value at the
    provided date (either ISO format or a datetime object).

    >>> tseries.get_value(date2)
    2.0

    >>> tseries.get_value('1970-01-02')
    2.0

    Multiple options are available for slicing and subsetting an existing time
    series object. The time series can be sliced by the positional indices of
    entries like a list and single-element time series can be created from
    integer, datetime or string keys. Chronological order is maintained
    regardless of the order of the key.

    >>> tseries[0::2]
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-03 00:00:00              3.00

    >>> tseries[0]
    date                            value
    1970-01-01 00:00:00              1.00

    >>> tseries[date3]
    date                            value
    1970-01-03 00:00:00              3.00

    >>> tseries['1970-01-03']
    date                            value
    1970-01-03 00:00:00              3.00

    Subsetting by iterables of positional indices, datetimes or strings is also
    supported.

    >>> tseries[[1,0]]
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00

    >>> tseries[['1970-01-03', '1970-01-02']]
    date                            value
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00

    Simple statistics can be computed from mean and variance methods.

    >>> tseries.mean()
    2.0

    >>> tseries.variance()
    1.0

    Time series overload basic arithmetic operations by applying set operations
    to dates, e.g. elementwise addition applies to union of dates by default,
    while multiplication applies to the intersection of dates.

    >>> date4 = datetime.fromisoformat('1970-01-04')
    >>> dates2 = (date1, date2, date4)
    >>> values2 = (1, 2, 4)
    >>> tseries2 = ts.TimeSeries(dates2, values2)

    >>> tseries
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00

    >>> tseries2
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-04 00:00:00              4.00

    >>> tseries + tseries2
    date                            value
    1970-01-01 00:00:00              2.00
    1970-01-02 00:00:00              4.00
    1970-01-03 00:00:00              3.00
    1970-01-04 00:00:00              4.00

    >>> tseries - tseries2
    date                            value
    1970-01-01 00:00:00              0.00
    1970-01-02 00:00:00              0.00
    1970-01-03 00:00:00              3.00
    1970-01-04 00:00:00             -4.00

    >>> tseries * tseries2
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              4.00

    Broadcasting to elementwise operations is supported for float-convertable
    values across these operations.

    >>> (1+tseries/2) ** (2*tseries2)
    date                            value
    1970-01-01 00:00:00              2.25
    1970-01-02 00:00:00             16.00

    The set operation and fill values can be chosen by calling methods directly
    and providing arguments.

    >>> tseries.add(tseries2, operation='intersection')
    date                            value
    1970-01-01 00:00:00              2.00
    1970-01-02 00:00:00              4.00

    The operator attribute allows for even more customizable applications of
    functions, with direct specification of function to apply, set operations
    and fill values for preprocessing time series. Aggregation functions can be
    implemented via the elementwise flag.

    >>> from timeseries.stats import crosscovariance
    >>> tseries.operator.custom(crosscovariance, tseries2, elementwise=False)
    0.5

    The above example computes the cross-covariance on the intersecting dates.
    This and the cross-correlation can alternatively be computed by calling
    their respective methods directly.

    >>> tseries.crosscovariance(tseries2)
    0.5

    >>> tseries.crosscorrelation(tseries2)
    1.0

    Basic filtering can be executed by direct calls to various methods. Support
    includes simple moving averages, exponential moving averages and rolling
    variance.

    >>> tseries.moving_average(window_size=2)
    date                            value
    1970-01-02 00:00:00              1.50
    1970-01-03 00:00:00              2.50

    >>> tseries.exponential_moving_average(alpha=0.1)
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              1.10
    1970-01-03 00:00:00              1.29

    >>> tseries.rolling_variance(2)
    date                            value
    1970-01-02 00:00:00              0.50
    1970-01-03 00:00:00              0.50

    More advanced filtering methods can be accessed via the rolling method,
    which provides an interface to customizable rolling window functionality,
    including variable weighting of values and custom functions.

    >>> tseries.rolling(2, weights='none').get_weights()
    [1, 1]

    >>> tseries.rolling(2, weights='none').custom(ts.stats.variance)
    date                            value
    1970-01-02 00:00:00              0.50
    1970-01-03 00:00:00              0.50

    >>> tseries.rolling(2, weights='none').sum()
    date                            value
    1970-01-02 00:00:00              3.00
    1970-01-03 00:00:00              5.00

    >>> tseries.rolling(2, weights='linear', min_weight=0.2).get_weights()
    [0.2, 0.8]

    >>> tseries.rolling(2, weights='linear', min_weight=0.2).sum()
    date                            value
    1970-01-02 00:00:00              1.80
    1970-01-03 00:00:00              2.80
    """
    def __init__(self, dates, values):
        """
        Initialize time series object.

        :param dates: finite-length iterable of datetime objects
        :param values: finite-length iterable of float-convertable numbers
        """
        # note: _ prefix indicates internal use, but user could theoretically
        # still directly access and modify / break this
        self._data = self._load_data(dates, values)

    def __repr__(self):
        # use explicit 'YYYY-MM-DD HH:MM:SS' format for consistency
        date_format = r'%Y-%m-%d %H:%M:%S'
        data = []
        date_string = ''
        for date, value in self._data.items():
            date_string = date.strftime(date_format)
            data.append('{} {:>17.2f}'.format(date_string, value))
        # use length of last date string to determine padding for header
        header = '{date_header:<{width}} {value_header:>17}\n'.format(
            date_header='date',
            value_header='value',
            width=len(date_string),
        )
        repr_string = header + '\n'.join(data)
        return repr_string

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if isinstance(other, TimeSeries):
            equals = self.dates == other.dates and self.values == other.values
        else:
            raise NotImplementedError(
                f'cannot assess equality against {type(other)}')
        return equals

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __rsub__(self, other):
        from timeseries.operator import right_subtract
        return self.operator.custom(right_subtract, other, 'union')

    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.divide(other)

    def __rtruediv__(self, other):
        from timeseries.operator import right_divide
        return self.operator.custom(right_divide, other, 'intersection')

    def __pow__(self, other):
        return self.power(other)

    def __rpow__(self, other):
        from timeseries.operator import right_power
        return self.operator.custom(right_power, other, 'intersection')

    def __getitem__(self, key):
        try:
            # use existing slice implementation for dates and values
            if isinstance(key, slice):
                dates = self.dates[key]
                values = self.values[key]
            # single-element access from integer position
            elif isinstance(key, int):
                date = self.dates[key]
                dates = (date,)
                values = (self.get_value(date),)
            # single-element access with get_value method
            elif isinstance(key, datetime) or isinstance(key, str):
                date = self._infer_date(key)
                dates = (date,)
                values = (self.get_value(date),)
            elif hasattr(key, '__iter__'):
                dates, values = list(), list()
                # multi-element access from iterable of integers
                if all(isinstance(item, int) for item in key):
                    for item in key:
                        date = self.dates[item]
                        dates.append(date)
                        values.append(self.get_value(date))
                else:
                    # last-resort: attempt iteration with get_value method
                    for item in key:
                        date = self._infer_date(item)
                        dates.append(date)
                        values.append(self.get_value(date))
            else:
                raise NotImplementedError(
                    f'cannot infer keys from \'{key}\'')
            # can be optimized - input validation in constructor is redundant
            return TimeSeries(dates, values)
        except Exception:
            raise IndexError('accessing time series elements failed')

    @property
    def dates(self):
        """
        Return tuple of time series dates.
        """
        return tuple(self._data.keys())

    @property
    def iso_dates(self):
        """
        Return tuple of time series dates in ISO format.
        """
        iso_dates = tuple(date.isoformat() for date in self._data.keys())
        return iso_dates

    @property
    def values(self):
        """
        Return tuple of time series values.
        """
        return tuple(self._data.values())

    @staticmethod
    def _load_data(dates, values):
        """
        Validate inputs and return sorted date-value pairs as dict.

        :param dates: finite-length iterable of datetime objects
        :param values: finite-length iterable of float-convertable numbers
        """
        # check that inputs are iterables with well-defined lengths
        def check_valid_iterable(iterable, input):
            if not hasattr(iterable, '__iter__'):
                raise IteratorError(f'{input} object is not iterable')
            if not hasattr(iterable, '__len__'):
                raise IteratorError(f'{input} object has no length')
        check_valid_iterable(dates, 'dates')
        check_valid_iterable(values, 'values')
        # validate input dimensions and dates
        if len(dates) is not len(values):
            raise InputDimensionError('dates and values must be the same size')
        if not all(isinstance(date, datetime) for date in dates):
            raise DateError('all dates must be datetime objects')
        if len(set(dates)) is not len(dates):
            raise DateError('all dates must be unique')
        # convert values to floats
        flt_values = []
        for value in values:
            try:
                flt_values.append(float(value))
            except ValueError:
                raise NumericValueError(
                    'all values must be convertable to floats')
        # store date-value pairs as dict sorted chronologically by date
        # note: SortedDict is more elegant but depends on third-party module
        data = {date: value for date, value in sorted(zip(dates, flt_values))}
        return data

    @staticmethod
    def _infer_date(date):
        """
        Return inferred datetime object.

        :param date: datetime object or string in ISO format
        """
        # infer date from ISO format if not datetime object
        if not isinstance(date, datetime):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                raise DateError(f'date inferral from \'{date}\' failed')
        return date

    def get_value(self, date):
        """
        Return value of time series at specified date.

        :param date: datetime object or string in ISO format
        """
        # infer date from ISO format if not datetime object
        date = self._infer_date(date)
        try:
            date_value = self._data[date]
        except Exception:
            raise KeyError(f'{date.isoformat()} not found in time series')
        return date_value

    def to_csv(self, filepath, **kwargs):
        """
        Write time series to CSV file.

        :param filepath: path of output file
        :param date_column: date column string, defaults to 'times'
        :param value_column: value column string, defaults to 'values'
        :param to_string: date format string or explicit function for string
            conversion, defaults to days since UNIX epoch
        :param ``**kwargs``: optional keyword arguments passed to DictWriter
        """
        from timeseries.io import to_csv
        to_csv(
            self,
            filepath,
            date_column='times',
            value_column='values',
            to_string=None,
            **kwargs,
        )
        return None

    def mean(self):
        """
        Return sample mean of time series.
        """
        from timeseries.stats import mean
        return mean(self.values)

    def variance(self):
        """
        Return sample variance of time series.
        """
        from timeseries.stats import variance
        return variance(self.values)

    def crosscovariance(self, other):
        """
        Return cross-covariance with time series on intersecting dates.

        :param other: time series or broadcastable argument to subtract
        """
        from timeseries.stats import crosscovariance
        self._intersect_warn(other)
        return self.operator.custom(crosscovariance, other, elementwise=False)

    def crosscorrelation(self, other):
        """
        Return cross-correlation with time series on intersecting dates.

        :param other: time series or broadcastable argument to subtract
        """
        from timeseries.stats import crosscorrelation
        self._intersect_warn(other)
        return self.operator.custom(crosscorrelation, other, elementwise=False)

    def _intersect_warn(self, other):
        if self.dates != other.dates:
            warnings.warn(
                'time series have different dates, computing on intersection')

    def rolling(self, window_size=1, weights='even', **kwargs):
        """
        Return rolling window object for customizable filtering.

        :param window_size: integer size of rolling window, defaults to 1
        :param weights: type of weights, defaults to 'even'. Current options:
            'even' - all points weighted evenly
            'linear' - weights increasing linearly from 'min_weight' parameter
            'none' - no weighting
        :param ``**kwargs``: keyword arguments passed to weights as parameters
        """
        from timeseries.filter.window import _RollingWindow
        return _RollingWindow(self, window_size, weights, **kwargs)

    def moving_average(self, window_size):
        """
        Return moving average.

        :param window_size: integer size of rolling window
        """
        return self.rolling(window_size, weights='even').sum()

    def rolling_variance(self, window_size):
        """
        Return rolling sample variance.

        :param window_size: integer size of rolling window
        """
        from timeseries.stats import variance
        return self.rolling(window_size, weights='none').custom(variance)

    def exponential_moving_average(self, alpha):
        """
        Return exponential moving average.

        :param alpha: smoothing factor, must be between 0 and 1
        """
        return self.rolling(weights='none').exponential_moving_average(alpha)

    @property
    def operator(self):
        """
        Return operator object for customizable function calls.
        """
        from timeseries.operator import _TimeSeriesOperator
        return _TimeSeriesOperator(self)

    def add(self, other, operation='union', fill=0):
        """
        Return element-wise summed time series after set operation.

        :param other: time series or broadcastable argument
        :param operation: set operation to apply to time series dates, defaults
            to  'union'
        :param fill: value to fill in missing dates, defaults to 0
        """
        from timeseries.operator import add
        return self.operator.custom(add, other, operation, fill=fill)

    def subtract(self, other, operation='union', fill=0):
        """
        Return element-wise subtracted time series after set operation.

        :param other: time series or broadcastable argument to subtract
        :param operation: set operation to apply to time series dates, defaults
            to  'union'
        :param fill: value to fill in missing dates, defaults to 0
        """
        from timeseries.operator import subtract
        return self.operator.custom(subtract, other, operation, fill=fill)

    def multiply(self, other, operation='intersection', fill=1):
        """
        Return element-wise multiplied time series after set operation.

        :param other: time series or broadcastable argument to subtract
        :param operation: set operation to apply to time series dates, defaults
            to  'intersection'
        :param fill: value to fill in missing dates, defaults to 1
        """
        from timeseries.operator import multiply
        return self.operator.custom(multiply, other, operation, fill=fill)

    def divide(self, other, operation='intersection', fill=1):
        """
        Return element-wise divided time series after set operation.

        :param other: time series or broadcastable argument to subtract
        :param operation: set operation to apply to time series dates, defaults
            to  'intersection'
        :param fill: value to fill in missing dates, defaults to 1
        """
        from timeseries.operator import divide
        return self.operator.custom(divide, other, operation, fill=fill)

    def power(self, other, operation='intersection', fill=1):
        """
        Return element-wise exponentiation of time series after set operation.

        :param other: time series or broadcastable argument for exponent
        :param operation: set operation to apply to time series dates, defaults
            to  'intersection'
        :param fill: value to fill in missing dates, defaults to 1
        """
        from timeseries.operator import power
        return self.operator.custom(power, other, operation, fill=fill)
