import warnings

from timeseries.errors import (
    FilteringWindowError,
)

from timeseries.filter.weights import (
    EvenWeights,
    LinearWeights,
    NoneWeights,
)

from timeseries.filter.func import (
    WindowFunction,
    SeriesFunction,
    CustomWindowFunction,
    SumWindow,
    CustomExponentialSeriesFunction,
    ExponentialMovingAverageSeries,
)


class _RollingWindow:
    """
    Rolling window class for applying filters to time series.
    """
    # map keys to weight classes
    _WEIGHTS = {
        'even': EvenWeights,
        'linear': LinearWeights,
        'none': NoneWeights,
    }
    # map keys to window function classes
    _WINDOWFUNCS = {
        'custom': CustomWindowFunction,
        'sum': SumWindow,
        'exponential_custom': CustomExponentialSeriesFunction,
        'exponential_moving_average': ExponentialMovingAverageSeries,
    }

    def __init__(self, tseries, window_size, weights='even', **kwargs):
        """
        Initialize rolling window object.

        :param tseries: time series object
        :param window_size: integer size of rolling window
        :param weights: type of weights, defaults to 'even'. Current options:
            'even' - all points weighted evenly
            'linear' - weights increasing linearly from 'min_weight' parameter
            'none' - no weighting
        :param '**kwargs': keyword arguments passed to weights as parameters
        """
        # check that specified weights are implemented
        if weights not in self._WEIGHTS.keys():
            raise KeyError(
                f'{weights} is not a valid choice of weights')
        # trust user to not modify these
        self._tseries = tseries
        self._weights_key = weights
        self._weights = self._WEIGHTS[weights](**kwargs)

        # window size validated in setter
        self.window_size = window_size

    @property
    def weights(self):
        return self._weights_key

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        # convert to float to ensure access to is_integer method
        try:
            flt_value = float(value)
        except TypeError:
            raise TypeError(f'\'{value}\' is not a valid window size')
        # validate numeric window size
        if not flt_value.is_integer():
            raise ValueError('window size must be integer')
        if not flt_value <= len(self._tseries):
            raise FilteringWindowError(
                'window size must be smaller than length of time series')
        if not flt_value > 0:
            raise ValueError(
                'window size must be at least 1')
        self._window_size = int(flt_value)

    def get_weights(self):
        return self._weights.get_weights(self.window_size)

    def _apply_filter(self, window_func, **kwargs):
        """
        Apply filter and return time series.

        :param window_func: windowed function to apply. Current options:
            'average' - weighted moving average over window size
        :param '**kwargs': keyword arguments passed to window function
        """
        from timeseries import TimeSeries
        ts_values = self._tseries.values
        # check that specified windowed function is implemented
        if window_func not in self._WINDOWFUNCS.keys():
            raise KeyError(
                f'{window_func} is not a valid choice of windowed function')
        _window_func = self._WINDOWFUNCS[window_func](**kwargs)
        # skip rolling window if window function returns values directly
        if isinstance(_window_func, SeriesFunction):
            if self._weights_key != 'none':
                warnings.warn(
                    'function computes values directly, weights are not used')
            dates = self._tseries.dates
            values = _window_func.apply_to_series(ts_values)
        elif isinstance(_window_func, WindowFunction):
            # initialize weights and dates
            weights = self.get_weights()
            dates = self._tseries.dates[self.window_size-1:]
            # create generator for shifted value ranges
            window_value_ranges = (
                ts_values[i:i+self.window_size]
                for i in range(len(self._tseries)+1-self.window_size)
            )
            values = list()
            for window_values in window_value_ranges:
                # weights applied to inputs before window function
                weighted_values = [weights[i]*window_values[i]
                                   for i in range(self.window_size)]
                # this could often be optimized by using caching / update rules
                value = _window_func.apply_to_window(weighted_values)
                values.append(value)
        else:
            raise TypeError(
                '_window_func must subclass WindowFunction or SeriesFunction')
        tseries = TimeSeries(dates, values)
        return tseries

    def custom(self, func):
        """
        Apply custom function to weighted values in rolling window and return
        time series.

        :param func: custom function to apply in rolling windows
        """
        return self._apply_filter('custom', func=func)

    def sum(self):
        """
        Sum weighted values in rolling window and return time series.
        """
        return self._apply_filter('sum')

    def exponential_custom(self, func, alpha):
        """
        Apply custom exponentially smoothed function and return time series.

        :param func: function to apply to series
        :param alpha: smoothing factor, must be between 0 and 1
        """
        return self._apply_filter('exponential_custom', func=func, alpha=alpha)

    def exponential_moving_average(self, alpha):
        """
        Sum weighted values in rolling window and return time series.

        :param alpha: smoothing factor, must be between 0 and 1
        """
        return self._apply_filter('exponential_moving_average', alpha=alpha)
