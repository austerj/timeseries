class IteratorError(ValueError):
    """
    Error raised when creating time series from non-iterable / no-length input.
    """


class InputDimensionError(ValueError):
    """
    Error raised when creating time series without matching input dimensions.
    """


class DateError(ValueError):
    """
    Error raised when creating time series with non-datetime or duplicate keys.
    """


class NumericValueError(ValueError):
    """
    Error raised when creating time series with non-numeric values.
    """
