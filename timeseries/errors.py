class IteratorError(ValueError):
    """
    Error raised when creating time series from non-iterable / no-length input.
    """


class InputDimensionError(IndexError):
    """
    Error raised when creating time series without matching input dimensions.
    """


class DateError(TypeError):
    """
    Error raised when creating time series with non-datetime or duplicate keys.
    """


class NumericValueError(TypeError):
    """
    Error raised when creating time series with non-numeric values.
    """


class CSVDateError(TypeError):
    """
    Error raised when unable to convert CSV dates to datetime objects.
    """


class CSVLoadError(RuntimeError):
    """
    Error raised when unable to load CSV file.
    """


class WeightsError(ValueError):
    """
    Error raised when providing invalid parameters to weights.
    """
