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
    Abstract class for applying function to whole series.
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
        Return result of custom function applied to window.

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
