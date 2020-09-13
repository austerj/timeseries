from abc import ABC, abstractmethod

from timeseries.errors import (
    WeightsError,
)


class Weights(ABC):
    """
    Abstract class for applying weights in rolling window.
    """
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_weights(self):
        pass


class EvenWeights(Weights):
    """
    Even (uniform) weights for rolling window.

    :example:
    >>> from timeseries.filter.weights import EvenWeights

    >>> EvenWeights().get_weights(4)
    [0.25, 0.25, 0.25, 0.25]

    >>> EvenWeights().get_weights(5)
    [0.2, 0.2, 0.2, 0.2, 0.2]
    """
    def get_weights(self, window_size):
        weights = [1/window_size for _ in range(window_size)]
        return weights


class LinearWeights(Weights):
    """
    Linearly increasing weights for rolling window.

    :example:
    >>> from timeseries.filter.weights import LinearWeights

    >>> LinearWeights(min_weight=0.1).get_weights(2)
    [0.1, 0.9]

    >>> LinearWeights(min_weight=0.1).get_weights(4)
    [0.1, 0.2, 0.3, 0.4]
    """
    def __init__(self, min_weight):
        """
        Initialize linearly increasing weights.

        :param min_weight: minimum weight to apply, must be between 0 and 1
        """
        if min_weight <= 0 or min_weight >= 1:
            raise WeightsError('use minimum weight between 0 and 1')
        self.min_weight = min_weight

    def get_weights(self, window_size):
        # partial sum of natural numbers from 1 to window_size-1
        partial_sum = window_size * (window_size-1) // 2
        # slope to ensure weights sum to one
        slope = (1 - window_size*self.min_weight) / partial_sum
        weights = [self.min_weight + slope*_ for _ in range(window_size)]
        return weights


class NoneWeights(Weights):
    """
    None-weights (all ones) for rolling window.

    :example:
    >>> from timeseries.filter.weights import NoneWeights

    >>> NoneWeights().get_weights(5)
    [1, 1, 1, 1, 1]
    """
    def get_weights(self, window_size):
        weights = [1 for _ in range(window_size)]
        return weights
