# commands/distributions.py
import discord
from discord.ext import commands
from ..utils.calculations import *
from ..utils.plotting import plot_distribution, save_plot_as_bytes
from ..utils.validators import validate_positive
from ..personality.responses import maho_response
import numpy as np
import matplotlib.pyplot as plt

def distributions_setup(bot):
    @bot.command(name='normal', help="Calculate normal distribution probability density. Usage: !normal [x] [mean] [std]")
    async def calc_normal(ctx, x: float, mean: float, std: float):
        try:
            result = normal_probability(x, mean, std)
            response = f"The probability density for x={x} in a normal distribution with mean={mean} and std={std} is {result:.6f}."
            response += "\nLook at you, using the bell curve like a pro. Don't let it go to your head."
            
            fig = plot_distribution(normal_probability, (mean, std), (mean-4*std, mean+4*std), 
                                    f"Normal Distribution (μ={mean}, σ={std})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'normal_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")


    @bot.command(name='normal_cdf', help="Calculate normal distribution cumulative probability. Usage: !normal_cdf [x] [mean] [std]")
    async def calc_normal_cdf(ctx, x: float, mean: float, std: float):
        try:
            result = normal_cdf(x, mean, std)
            response = f"The cumulative probability for x≤{x} in a normal distribution with mean={mean} and std={std} is {result:.6f}."
            response += "\nCongratulations, you can now calculate the area under a curve. Your parents must be so proud."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='exponential', help="Calculate exponential distribution probability density. Usage: !exponential [x] [scale]")
    async def calc_exponential(ctx, x: float, scale: float):
        try:
            result = exponential_probability(x, scale)
            response = f"The probability density for x={x} in an exponential distribution with scale={scale} is {result:.6f}."
            response += "\nExponential decay, just like your patience for these distributions, I bet."
            
            fig = plot_distribution(exponential_probability, (scale,), (0, scale*5), 
                                    f"Exponential Distribution (scale={scale})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'exponential_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='gamma', help="Calculate gamma distribution probability density. Usage: !gamma [x] [shape] [scale]")
    async def calc_gamma(ctx, x: float, shape: float, scale: float):
        try:
            result = gamma_probability(x, shape, scale)
            response = f"The probability density for x={x} in a gamma distribution with shape={shape} and scale={scale} is {result:.6f}."
            response += "\nGamma distribution, because sometimes life is too complex for simple exponentials."
            
            fig = plot_distribution(gamma_probability, (shape, scale), (0, shape*scale*5), 
                                    f"Gamma Distribution (shape={shape}, scale={scale})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'gamma_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='beta', help="Calculate beta distribution probability density. Usage: !beta [x] [a] [b]")
    async def calc_beta(ctx, x: float, a: float, b: float):
        try:
            result = beta_probability(x, a, b)
            response = f"The probability density for x={x} in a beta distribution with a={a} and b={b} is {result:.6f}."
            response += "\nBeta distribution: for when you want to confine your ignorance to the interval [0, 1]."
            
            fig = plot_distribution(beta_probability, (a, b), (0, 1), 
                                    f"Beta Distribution (a={a}, b={b})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'beta_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='uniform', help="Calculate uniform distribution probability density. Usage: !uniform [x] [low] [high]")
    async def calc_uniform(ctx, x: float, low: float, high: float):
        try:
            result = uniform_probability(x, low, high)
            response = f"The probability density for x={x} in a uniform distribution between {low} and {high} is {result:.6f}."
            response += "\nUniform distribution: when you have no clue and you're proud of it."
            
            fig = plot_distribution(uniform_probability, (low, high), (low, high), 
                                    f"Uniform Distribution ({low}, {high})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'uniform_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='t_dist', help="Calculate t-distribution probability density. Usage: !t_dist [x] [df]")
    async def calc_t_dist(ctx, x: float, df: float):
        try:
            result = t_probability(x, df)
            response = f"The probability density for x={x} in a t-distribution with {df} degrees of freedom is {result:.6f}."
            response += "\nT-distribution: for when normal just isn't student enough for you."
            
            fig = plot_distribution(t_probability, (df,), (-4, 4), 
                                    f"T-Distribution (df={df})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 't_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='f_dist', help="Calculate F-distribution probability density. Usage: !f_dist [x] [dfn] [dfd]")
    async def calc_f_dist(ctx, x: float, dfn: float, dfd: float):
        try:
            result = f_probability(x, dfn, dfd)
            response = f"The probability density for x={x} in an F-distribution with dfn={dfn} and dfd={dfd} is {result:.6f}."
            response += "\nF-distribution: because sometimes you need to compare variances, and life isn't complicated enough."
            
            fig = plot_distribution(f_probability, (dfn, dfd), (0, 5), 
                                    f"F-Distribution (dfn={dfn}, dfd={dfd})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'f_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='chi2_dist', help="Calculate chi-squared distribution probability density. Usage: !chi2_dist [x] [df]")
    async def calc_chi2_dist(ctx, x: float, df: float):
        try:
            result = chi2_probability(x, df)
            response = f"The probability density for x={x} in a chi-squared distribution with {df} degrees of freedom is {result:.6f}."
            response += "\nChi-squared distribution: for when you want to test goodness-of-fit, or just fit some squared normal variables."
            
            fig = plot_distribution(chi2_probability, (df,), (0, max(5, df*2)), 
                                    f"Chi-squared Distribution (df={df})")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'chi2_distribution.png'))
            plt.close(fig)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='normal_quantile', help="Calculate normal distribution quantile. Usage: !normal_quantile [p] [mean] [std]")
    async def calc_normal_quantile(ctx, p: float, mean: float, std: float):
        try:
            result = normal_quantile(p, mean, std)
            response = f"The {p*100}th percentile of a normal distribution with mean={mean} and std={std} is {result:.6f}."
            response += "\nCongratulations, you can now find specific points on a bell curve. Your life is complete."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='exponential_quantile', help="Calculate exponential distribution quantile. Usage: !exponential_quantile [p] [scale]")
    async def calc_exponential_quantile(ctx, p: float, scale: float):
        try:
            result = exponential_quantile(p, scale)
            response = f"The {p*100}th percentile of an exponential distribution with scale={scale} is {result:.6f}."
            response += "\nExponential decay, just like my patience for these quantile calculations."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='gamma_quantile', help="Calculate gamma distribution quantile. Usage: !gamma_quantile [p] [shape] [scale]")
    async def calc_gamma_quantile(ctx, p: float, shape: float, scale: float):
        try:
            result = gamma_quantile(p, shape, scale)
            response = f"The {p*100}th percentile of a gamma distribution with shape={shape} and scale={scale} is {result:.6f}."
            response += "\nGamma quantiles, for when you really want to complicate your life."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='beta_quantile', help="Calculate beta distribution quantile. Usage: !beta_quantile [p] [a] [b]")
    async def calc_beta_quantile(ctx, p: float, a: float, b: float):
        try:
            result = beta_quantile(p, a, b)
            response = f"The {p*100}th percentile of a beta distribution with a={a} and b={b} is {result:.6f}."
            response += "\nBeta quantiles: because sometimes you need to find specific points in your [0, 1] ignorance."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='uniform_quantile', help="Calculate uniform distribution quantile. Usage: !uniform_quantile [p] [low] [high]")
    async def calc_uniform_quantile(ctx, p: float, low: float, high: float):
        try:
            result = uniform_quantile(p, low, high)
            response = f"The {p*100}th percentile of a uniform distribution between {low} and {high} is {result:.6f}."
            response += "\nUniform quantiles: when you want to pretend your ignorance is evenly distributed."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")


    @bot.command(name='ci', help="Calculate confidence interval. Usage: !ci [type] [parameters]")
    async def confidence_interval(ctx, ci_type: str, *args):
        try:
            if ci_type == "mean":
                # !ci mean [sample_mean] [sample_std] [sample_size] [confidence_level]
                mean, std, n, conf_level = map(safe_float_conversion, args)
                validate_positive(std, "Sample standard deviation")
                validate_positive(n, "Sample size")
                if not 0 < conf_level < 1:
                    raise commands.BadArgument("Confidence level must be between 0 and 1.")
                margin = stats.t.ppf((1 + conf_level) / 2, n - 1) * (std / np.sqrt(n))
                lower, upper = mean - margin, mean + margin
            elif ci_type == "proportion":
                # !ci proportion [successes] [sample_size] [confidence_level]
                successes, n, conf_level = map(safe_float_conversion, args)
                validate_positive(successes, "Number of successes")
                validate_positive(n, "Sample size")
                if not 0 < conf_level < 1:
                    raise commands.BadArgument("Confidence level must be between 0 and 1.")
                p = successes / n
                margin = stats.norm.ppf((1 + conf_level) / 2) * np.sqrt(p * (1 - p) / n)
                lower, upper = p - margin, p + margin
            elif ci_type == "difference":
                # !ci difference [mean1] [std1] [n1] [mean2] [std2] [n2] [confidence_level]
                mean1, std1, n1, mean2, std2, n2, conf_level = map(safe_float_conversion, args)
                validate_positive(std1, "Standard deviation of group 1")
                validate_positive(std2, "Standard deviation of group 2")
                validate_positive(n1, "Sample size of group 1")
                validate_positive(n2, "Sample size of group 2")
                if not 0 < conf_level < 1:
                    raise commands.BadArgument("Confidence level must be between 0 and 1.")
                se = np.sqrt(std1**2 / n1 + std2**2 / n2)
                margin = stats.t.ppf((1 + conf_level) / 2, n1 + n2 - 2) * se
                diff = mean1 - mean2
                lower, upper = diff - margin, diff + margin
            else:
                raise commands.BadArgument("Invalid CI type. Use 'mean', 'proportion', or 'difference'.")

            result = f"{conf_level*100}% Confidence Interval: ({lower:.4f}, {upper:.4f})"
            response = f"Ugh, fine. Here's your precious confidence interval:\n\n{result}\n\nHappy now? Don't expect me to interpret it for you."
            await ctx.send(response)
        except Exception as e:
            raise commands.BadArgument(f"Are you trying to break me? Your input is invalid. Error: {str(e)}")



    # Add other distribution commands (exponential, gamma, beta, uniform) here...
    # The structure will be similar to the normal distribution command