from abc import ABC, abstractmethod


class WindowFunction(ABC):
    """
    Abstract class for applying function in window.
    """
    def __init__(self, rolling=True, *args, **kwargs):
        # flag for rolling windows - set to False if window function returns
        # full series of values directly, e.g. for exponential MA
        self.rolling = True

    @abstractmethod
    def apply_to_window(self, values):
        pass


class CustomWindowFunction(WindowFunction):
    """
    Apply custom function to window.
    """
    def __init__(self, func):
        """
        Initialize custom window function.

        :param func: function to apply to window
        """
        super().__init__()
        self.func = func

    def apply_to_window(self, values):
        """
        Return result of custom function applied to window.

        :param values: values to apply function to
        """
        func_values = self.func(values)
        return func_values


class SumWindow(WindowFunction):
    """
    Sum over values in window.
    """
    def __init__(self):
        """
        Initialize sum window function.
        """
        super().__init__()

    def apply_to_window(self, values):
        """
        Return sum of values in window.

        :param values: values to apply function to
        """
        sum_values = sum(values)
        return sum_values
