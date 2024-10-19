import math
from scipy import stats
import numpy as np

def safe_float_conversion(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number.")

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers. Did you fail elementary math?")
    return math.factorial(n)

def combination(n, k):
    if n < k:
        raise ValueError("n must be greater than or equal to k. Basic combinatorics, come on!")
    return math.comb(n, k)

def permutation(n, k):
    if n < k:
        raise ValueError("n must be greater than or equal to k. Arrangement 101, get it right!")
    return math.perm(n, k)

def binomial_probability(n, k, p):
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Probability basics, seriously?")
    return stats.binom.pmf(k, n, p)

def poisson_probability(k, lambda_):
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive. Do you even Poisson, bro?")
    return stats.poisson.pmf(k, lambda_)

def normal_probability(x, mean, std):
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Did you skip Statistics 101?")
    return stats.norm.pdf(x, mean, std)

def normal_cdf(x, mean, std):
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Brush up on your basics!")
    return stats.norm.cdf(x, mean, std)

def exponential_probability(x, scale):
    if scale <= 0:
        raise ValueError("Scale parameter must be positive. Exponential decay, not growth!")
    return stats.expon.pdf(x, scale=scale)

def gamma_probability(x, shape, scale):
    if shape <= 0 or scale <= 0:
        raise ValueError("Shape and scale parameters must be positive. It's called 'positive' for a reason!")
    return stats.gamma.pdf(x, a=shape, scale=scale)

def beta_probability(x, a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Both shape parameters must be positive. Beta is picky like that.")
    return stats.beta.pdf(x, a, b)

def uniform_probability(x, low, high):
    if low >= high:
        raise ValueError("Upper bound must be greater than lower bound. Did you mix them up?")
    return stats.uniform.pdf(x, loc=low, scale=high-low)

def t_probability(x, df):
    """Calculate the probability density for a t-distribution."""
    if df <= 0:
        raise ValueError("Degrees of freedom must be positive. T-distribution 101, pay attention!")
    return stats.t.pdf(x, df)

def f_probability(x, dfn, dfd):
    """Calculate the probability density for an F-distribution."""
    if dfn <= 0 or dfd <= 0:
        raise ValueError("Degrees of freedom must be positive. F-distribution basics, come on!")
    return stats.f.pdf(x, dfn, dfd)

def chi2_probability(x, df):
    """Calculate the probability density for a chi-squared distribution."""
    if df <= 0:
        raise ValueError("Degrees of freedom must be positive. Chi-squared 101, get it right!")
    return stats.chi2.pdf(x, df)

def normal_quantile(p, mean, std):
    """Calculate the quantile (inverse CDF) for a normal distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Basic probability, remember?")
    if std <= 0:
        raise ValueError("Standard deviation must be positive. Did you fail Stats 101?")
    return stats.norm.ppf(p, loc=mean, scale=std)

def exponential_quantile(p, scale):
    """Calculate the quantile (inverse CDF) for an exponential distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. It's not rocket science!")
    if scale <= 0:
        raise ValueError("Scale parameter must be positive. Exponential decay, not growth!")
    return stats.expon.ppf(p, scale=scale)

def gamma_quantile(p, shape, scale):
    """Calculate the quantile (inverse CDF) for a gamma distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Do I need to explain probability to you?")
    if shape <= 0 or scale <= 0:
        raise ValueError("Shape and scale parameters must be positive. It's called 'positive' for a reason!")
    return stats.gamma.ppf(p, a=shape, scale=scale)

def beta_quantile(p, a, b):
    """Calculate the quantile (inverse CDF) for a beta distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. Probability 101, come on!")
    if a <= 0 or b <= 0:
        raise ValueError("Both shape parameters must be positive. Beta is picky like that.")
    return stats.beta.ppf(p, a, b)

def uniform_quantile(p, low, high):
    """Calculate the quantile (inverse CDF) for a uniform distribution."""
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1. It's a simple concept, really.")
    if low >= high:
        raise ValueError("Upper bound must be greater than lower bound. Did you mix them up?")
    return stats.uniform.ppf(p, loc=low, scale=high-low)