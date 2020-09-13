def mean(values):
    """
    Return the sample mean of a numeric iterable.

    :param values: finite-length iterable of float-convertable numbers

    :example:
    >>> import timeseries as ts

    >>> values = (1, 2, 3)
    >>> ts.stats.mean(values)
    2.0
    """
    sample_mean = sum(values) / len(values)
    return sample_mean


def variance(values):
    """
    Return the unbiased sample variance of a numeric iterable.

    :param values: finite-length iterable of float-convertable numbers

    :example:
    >>> import timeseries as ts

    >>> values = (1, 2, 3)
    >>> ts.stats.variance(values)
    1.0
    """
    sample_mean = mean(values)
    squared_deviations = [(value-sample_mean)**2 for value in values]
    biased_sample_variance = mean(squared_deviations)
    # using Bessel correction - bias is negligible for large samples
    bias_correction = len(values) / (len(values)-1)
    sample_variance = bias_correction*biased_sample_variance
    return sample_variance


def crosscovariance(values1, values2):
    """
    Return the (unnormalized) cross-covariance of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers

    :example:
    >>> import timeseries as ts

    >>> values1 = (1, 2, 3)
    >>> values2 = (-2, -4, -6)
    >>> ts.stats.crosscovariance(values1, values2)
    -2.0
    """
    sample_mean1 = mean(values1)
    sample_mean2 = mean(values2)
    product_deviations = [(value1-sample_mean1) * (value2-sample_mean2)
                          for value1, value2 in zip(values1, values2)]
    biased_sample_crosscovariance = mean(product_deviations)
    # using Bessel correction - bias is negligible for large samples
    bias_correction = len(values1) / (len(values1)-1)
    sample_crosscovariance = bias_correction*biased_sample_crosscovariance
    return sample_crosscovariance


def crosscorrelation(values1, values2):
    """
    Return the (normalized) Pearson cross-correlation of two numeric iterables.

    :param values1: finite-length iterable of float-convertable numbers
    :param values2: finite-length iterable of float-convertable numbers

    :example:
    >>> import timeseries as ts

    >>> values1 = (1, 2, 3)
    >>> values2 = (-2, -4, -6)
    >>> ts.stats.crosscorrelation(values1, values2)
    -1.0
    """
    sample_variance1 = variance(values1)
    sample_variance2 = variance(values2)
    if sample_variance1 <= 0 or sample_variance2 <= 0:
        raise ZeroDivisionError(
            'cannot compute cross-correlation for zero-variance series')
    normalization_factor = 1 / (sample_variance1*sample_variance2)**0.5
    # effectively computing means twice - can be optimized
    sample_crosscovariance = crosscovariance(values1, values2)
    sample_crosscorrelation = normalization_factor*sample_crosscovariance
    return sample_crosscorrelation


def adf_test(values, significance=0.05):
    """
    Return the augmented Dickey-Fuller unit root test statistic and result.

    :param values: finite-length iterable of float-convertable numbers
    :param significance: level of significance, defaults to 0.05
    """
    raise NotImplementedError()
