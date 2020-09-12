import csv
from collections.abc import Callable
from datetime import (
    datetime,
    timedelta,
    timezone,
)

import timeseries as ts
from timeseries.errors import (
        CSVLoadError,
        CSVDateError,
)


def read_csv(
    filepath,
    date_column='times',
    value_column='values',
    to_datetime=None,
    **kwargs,
):
    """
    Read CSV file and return time series.

    :param filepath: path of CSV file
    :param date_column: date column string, defaults to 'times'
    :param value_column: value column string, defaults to 'values'
    :param to_datetime: date format string or explicit function for datetime
        conversion, defaults to days since UNIX epoch
    :param '**kwargs': optional keyword arguments passed to DictReader

    :example:
    >>> import timeseries as ts

    >>> ts.read_csv(ts.samples_path + 'epoch.csv')
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00

    >>> ts.read_csv(ts.samples_path + 'iso.csv', to_datetime='%Y-%m-%d')
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00

    >>> ts.read_csv(ts.samples_path + 'epoch_semicolon.csv', delimiter=';')
    date                            value
    1970-01-01 00:00:00              1.00
    1970-01-02 00:00:00              2.00
    1970-01-03 00:00:00              3.00
    """
    # default datetime conversion using offset days from epoch
    if not to_datetime:
        unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

        def _to_datetime(days_since_epoch):
            # convert input to float and return datetime object
            try:
                days_since_epoch = float(days_since_epoch)
            except ValueError:
                raise CSVDateError('day offsets must be convertable to floats')
            date = unix_epoch + timedelta(days=days_since_epoch)
            return date
    # create datetime converter from string if no function is provided
    elif not isinstance(to_datetime, Callable):
        if not type(to_datetime) is str:
            raise CSVDateError((
                'Invalid datetime converter, provide explicit function or '
                '\'strptime\' compatible formatting string'))

        def _to_datetime(date_string):
            # convert input to str and return datetime with user string format
            date_string = str(date_string)
            date = datetime.strptime(date_string, to_datetime)
            return date
    else:
        _to_datetime = to_datetime

    def read_row(row, column):
        # read 'column' from row and catch exception
        try:
            output = row[column]
        except KeyError:
            raise CSVLoadError(f'\'{column}\' does not match header')
        return output
    # read file into lists of dates and values
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile, **kwargs)
            dates, values = list(), list()
            for row in reader:
                date_input = read_row(row, date_column)
                value = read_row(row, value_column)
                # convert to datetime
                try:
                    date = _to_datetime(date_input)
                except Exception:
                    raise CSVDateError('conversion to datetime failed')
                dates.append(date)
                values.append(value)
    except Exception:
        raise CSVLoadError('reading CSV file failed')
    tseries = ts.TimeSeries(dates, values)
    return tseries


def to_csv(
    tseries,
    filepath,
    date_column='times',
    value_column='values',
    to_string=None,
    **kwargs,
):
    """
    Write time series to CSV file.

    :param tseries: time series object
    :param filepath: path of output file
    :param date_column: date column string, defaults to 'times'
    :param value_column: value column string, defaults to 'values'
    :param to_string: date format string or explicit function for string
        conversion, defaults to days since UNIX epoch
    :param '**kwargs': optional keyword arguments passed to DictWriter
    """
    raise NotImplementedError()
