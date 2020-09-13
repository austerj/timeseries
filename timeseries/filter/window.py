from timeseries.filter.weights import (
    EvenWeights,
    LinearWeights,
)


class RollingWindow:
    # map keys to weight classes
    _WEIGHTS = {
        'even': EvenWeights,
        'linear': LinearWeights,
    }

    def __init__(self, tseries, window_size, weights='even', **kwargs):
        """
        Rolling window class for applying filters to time series.

        :param tseries: time series object
        :param window_size: integer size of rolling window
        :param weights: type of weights, defaults to 'even'. Current options:
            'even' - all points weighted evenly
            'linear' - weights increasing linearly from 'min_weight' parameter
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
            raise ValueError(
                'window size must be smaller than length of time series')
        if not flt_value > 0:
            raise ValueError(
                'window size must be at least 1')
        self._window_size = int(flt_value)

    def get_weights(self):
        return self._weights.get_weights(self.window_size)
