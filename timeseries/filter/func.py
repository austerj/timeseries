from abc import ABC, abstractmethod


class WindowFunction(ABC):
    """
    Abstract class for applying function in window.
    """
    @abstractmethod
    def apply_to_window(self, values):
        pass


class SeriesFunction(ABC):
    """
    Abstract class for applying function to series.
    """
    @abstractmethod
    def apply_to_series(self, values):
        pass


class CustomWindowFunction(WindowFunction):
    """
    Apply custom function in window.
    """
    def __init__(self, func):
        """
        Initialize custom window function.

        :param func: function to apply in window
        """
        super().__init__()
        self.func = func

    def apply_to_window(self, values):
        """
        Return result of function applied in window.

        :param values: values to apply function to
        """
        func_values = self.func(values)
        return func_values


class SumWindow(CustomWindowFunction):
    """
    Sum over values in window.
    """
    def __init__(self):
        """
        Initialize sum window function.
        """
        def sum_func(x): return sum(x)
        super().__init__(sum_func)


class CustomExponentialSeriesFunction(SeriesFunction):
    """
    Apply custom exponentially smoothed function to series.
    """
    def __init__(self, func, alpha):
        """
        Initialize custom series function.

        :param func: function to apply to series
        :param alpha: smoothing factor, must be between 0 and 1
        """
        super().__init__()
        self.func = func
        if alpha <= 0 or alpha > 1:
            raise ValueError('use smoothing factor between 0 and 1')
        self.alpha = alpha

    def apply_to_series(self, values):
        """
        Return result of exponentially smoothed function applied to series.

        :param values: values to apply function to
        """
        func_values = [self.func(value) for value in values]
        smoothed_func_values = self.exponential_moving_average(func_values)
        return smoothed_func_values

    def exponential_moving_average(self, values):
        """
        Return exponential moving average of values.

        :param values: values to apply function to
        """
        # initialize series
        smoothed_value = values[0]
        smoothed_values = [smoothed_value]
        # compute remainder of series recursively
        for value in values[1:]:
            smoothed_value *= 1-self.alpha
            smoothed_value += self.alpha*value
            smoothed_values.append(smoothed_value)
        # no adjustment for early weights - can be improved
        return smoothed_values


class ExponentialMovingAverageSeries(CustomExponentialSeriesFunction):
    """
    Exponentially smoothed moving average of series.
    """
    def __init__(self, alpha):
        """
        Initialize exponential moving average function.
        """
        def identity(x): return x
        super().__init__(identity, alpha)
