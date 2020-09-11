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

    Time series data is automatically sorted in chronological order by date.

    :example:
    >>> from datetime import datetime
    >>> import timeseries as ts
    >>> date1 = datetime.fromisoformat('1970-01-01')
    >>> date2 = datetime.fromisoformat('1970-01-02')
    >>> date3 = datetime.fromisoformat('1970-01-03')
    >>> dates = (date2, date1, date3)
    >>> values = (2, 1, 3)
    >>> tseries = ts.TimeSeries(dates, values)

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

    >>> tseries.get_value(date2)
    2.0

    >>> tseries.get_value('1970-01-02')
    2.0
    """

    def __init__(self, dates, values):
        """
        Initialize time series object.

        :param dates: iterable of datetime objects
        :param values: iterable of valid floating-point numbers
        """
        self._data = self._load_data(dates, values)

    def __repr__(self):
        """
        Return string representation of time series object.
        """
        header = '{:<19} {:>17}\n'.format('date', 'value')
        data = []
        for date, value in self._data.items():
            data.append('{} {:>17.2f}'.format(date, value))
        return header + '\n'.join(data)

    def __len__(self):
        """
        Return number of entries in time series.
        """
        return len(self._data)

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

    def _load_data(self, dates, values):
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
            except ValueError as e:
                raise NumericValueError(
                    f'{e.args[0]}, all values must be convertable to floats')
        # store date-value pairs as dict sorted chronologically by date
        # note: SortedDict is more elegant but depends on third-party module
        data = {date: value for date, value in sorted(zip(dates, flt_values))}
        return data

    def get_value(self, date):
        """
        Return value of time series at specified date.

        :param date: datetime object or string in ISO format
        """
        if not type(date) is datetime:
            try:
                date = datetime.fromisoformat(date)
            except ValueError as e:
                raise DateError(e.args[0])
        try:
            date_value = self._data[date]
        except KeyError:
            raise KeyError(f'{date.isoformat()} not found in time series')
        return date_value
