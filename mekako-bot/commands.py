# commands.py
import random
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib.parse
import discord
from discord.ext import commands
from utils import *

def setup_commands(bot):
    @bot.command(name='introduce', help="Ask Mekako to introduce herself")
    async def introduce(ctx):
        introduction = ("I'm Mekako, a statistics and probability bot. "
                        "Don't expect me to hold your hand through everything. "
                        "I'm here to help with complex calculations, not to be your friend. "
                        "But... I suppose if you have questions, I can try to answer them. "
                        "Just don't waste my time with trivial matters!")
        await ctx.send(introduction)

    @bot.command(name='praise', help="Praise Mekako (if you dare)")
    async def praise(ctx):
        responses = [
            "W-what are you saying all of a sudden? It's not like I need your approval!",
            "Of course I'm amazing. Did you just now notice?",
            "D-don't think this means anything! I'm just doing my job!",
            "Hmph, I suppose you're not so bad yourself... for a human."
        ]
        await ctx.send(random.choice(responses))

    @bot.command(name='hug', help="Try to hug Mekako (at your own risk)")
    async def hug(ctx):
        responses = [
            "W-what do you think you're doing?! I didn't give you permission for that!",
            "H-hey! Personal space, you know! ...I didn't say stop though.",
            "Ugh, fine. One hug. But don't get used to it!",
            "*begrudgingly accepts the hug* This doesn't mean anything, got it?"
        ]
        await ctx.send(random.choice(responses))

    @bot.command(name='ztest', help="One-sample z-test. Usage: !ztest [sample_mean] [population_mean] [population_std] [sample_size]")
    async def z_test(ctx, sample_mean: safe_float_conversion, population_mean: safe_float_conversion, 
                     population_std: safe_float_conversion, sample_size: int):
        validate_positive(population_std, "Population standard deviation")
        validate_positive(sample_size, "Sample size")

        z_statistic = (sample_mean - population_mean) / (population_std / np.sqrt(sample_size))
        p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))
        
        result = f"Z-statistic: {z_statistic:.4f}\nP-value: {p_value:.4f}"
        conclusion = "reject" if p_value < 0.05 else "fail to reject"
        
        response = maho_response("z-test", result, conclusion)
        
        setup_3b1b_style()
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x, 0, 1)
        ax.plot(x, y, color='#FFD56F')
        ax.fill_between(x[x <= -abs(z_statistic)], y[x <= -abs(z_statistic)], color='#FF7B54', alpha=0.3)
        ax.fill_between(x[x >= abs(z_statistic)], y[x >= abs(z_statistic)], color='#FF7B54', alpha=0.3)
        ax.set_title('Z-Test Visualization (try not to get overwhelmed)', fontsize=16, pad=20)
        ax.set_xlabel('Z-score')
        ax.set_ylabel('Probability Density')
        ax.axvline(z_statistic, color='#939B62', linestyle='--', label='Observed Z')
        ax.legend()
        
        buf = save_plot_as_bytes(fig)
        await ctx.send(response, file=discord.File(buf, 'z_test_plot.png'))
        plt.close(fig)

    @bot.command(name='ttest', help="One-sample t-test. Usage: !ttest [sample_mean] [population_mean] [sample_std] [sample_size]")
    async def t_test(ctx, sample_mean: safe_float_conversion, population_mean: safe_float_conversion, 
                     sample_std: safe_float_conversion, sample_size: int):
        validate_positive(sample_std, "Sample standard deviation")
        validate_positive(sample_size, "Sample size")

        t_statistic = (sample_mean - population_mean) / (sample_std / np.sqrt(sample_size))
        df = sample_size - 1
        p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))
        
        result = f"T-statistic: {t_statistic:.4f}\nDegrees of freedom: {df}\nP-value: {p_value:.4f}"
        conclusion = "reject" if p_value < 0.05 else "fail to reject"
        
        response = maho_response("t-test", result, conclusion)
        
        setup_3b1b_style()
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(-4, 4, 1000)
        y = stats.t.pdf(x, df)
        ax.plot(x, y, color='#FFD56F')
        ax.fill_between(x[x <= -abs(t_statistic)], y[x <= -abs(t_statistic)], color='#FF7B54', alpha=0.3)
        ax.fill_between(x[x >= abs(t_statistic)], y[x >= abs(t_statistic)], color='#FF7B54', alpha=0.3)
        ax.set_title('T-Test Visualization (as if you understand it)', fontsize=16, pad=20)
        ax.set_xlabel('T-score')
        ax.set_ylabel('Probability Density')
        ax.axvline(t_statistic, color='#939B62', linestyle='--', label='Observed T')
        ax.legend()
        
        buf = save_plot_as_bytes(fig)
        await ctx.send(response, file=discord.File(buf, 't_test_plot.png'))
        plt.close(fig)

    @bot.command(name='chisquare', help="Chi-square goodness of fit test. Usage: !chisquare [observed_freq1,obs2,...] [expected_freq1,exp2,...]")
    async def chi_square_test(ctx, observed: str, expected: str):
        try:
            observed = [safe_float_conversion(x) for x in observed.split(',')]
            expected = [safe_float_conversion(x) for x in expected.split(',')]
            
            if len(observed) != len(expected):
                raise ValueError("Observed and expected frequencies must have the same length. Can't you count?")
            
            chi2_statistic, p_value = stats.chisquare(observed, expected)
            
            result = f"Chi-square statistic: {chi2_statistic:.4f}\nDegrees of freedom: {len(observed)-1}\nP-value: {p_value:.4f}"
            conclusion = "reject" if p_value < 0.05 else "fail to reject"
            
            response = maho_response("chi-square test", result, conclusion)
            
            setup_3b1b_style()
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.arange(len(observed))
            width = 0.35
            ax.bar(x - width/2, observed, width, label='Observed', color='#FF7B54')
            ax.bar(x + width/2, expected, width, label='Expected', color='#FFD56F')
            ax.set_xlabel('Categories')
            ax.set_ylabel('Frequencies')
            ax.set_title('Chi-square Test: Observed vs Expected (pay attention!)', fontsize=16, pad=20)
            ax.legend()
            
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'chi_square_test_plot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error performing chi-square test: {str(e)}. Maybe stick to simpler tests?")
            
            buf = save_plot_as_bytes()
            await ctx.send(response, file=discord.File(buf, 'chi_square_test_plot.png'))
            plt.close()
        except Exception as e:
            raise commands.BadArgument(f"Invalid input. Seriously, is it that hard to enter numbers correctly? Error: {str(e)}")

    @bot.command(name='anova', help="One-way ANOVA. Usage: !anova [group1: x1,x2,...] [group2: y1,y2,...] ...")
    async def anova_test(ctx, *args):
        try:
            data = [list(map(safe_float_conversion, group.split(':')[1].split(','))) for group in args]
            group_names = [group.split(':')[0] for group in args]
            
            if len(data) < 2:
                raise ValueError("At least two groups are required for ANOVA. Did you miss a group?")
            
            f_statistic, p_value = stats.f_oneway(*data)
            
            result = f"F-statistic: {f_statistic:.4f}\nP-value: {p_value:.4f}"
            conclusion = "reject" if p_value < 0.05 else "fail to reject"
            
            response = maho_response("one-way ANOVA", result, conclusion)
            
            fig = plot_3b1b_boxplot(data, group_names, "One-way ANOVA: Distribution of Groups")
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'anova_plot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error performing ANOVA: {str(e)}. Maybe you should review your basic statistics?")

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

    @bot.command(name='ttest2', help="Two-sample t-test. Usage: !ttest2 [type] [parameters]")
    async def two_sample_ttest(ctx, test_type: str, *args):
        try:
            if test_type == "independent":
                # !ttest2 independent [mean1] [std1] [n1] [mean2] [std2] [n2]
                mean1, std1, n1, mean2, std2, n2 = map(safe_float_conversion, args)
                validate_positive(std1, "Standard deviation of group 1")
                validate_positive(std2, "Standard deviation of group 2")
                validate_positive(n1, "Sample size of group 1")
                validate_positive(n2, "Sample size of group 2")
                t_stat, p_value = stats.ttest_ind_from_stats(mean1, std1, n1, mean2, std2, n2)
            elif test_type == "paired":
                # !ttest2 paired [difference_mean] [difference_std] [n]
                diff_mean, diff_std, n = map(safe_float_conversion, args)
                validate_positive(diff_std, "Standard deviation of differences")
                validate_positive(n, "Sample size")
                t_stat = diff_mean / (diff_std / np.sqrt(n))
                p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))
            else:
                raise commands.BadArgument("Invalid test type. Use 'independent' or 'paired'.")

            result = f"T-statistic: {t_stat:.4f}\nP-value: {p_value:.4f}"
            conclusion = "reject" if p_value < 0.05 else "fail to reject"
            response = maho_response("two-sample t-test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            raise commands.BadArgument(f"Seriously? Your input is so bad I can't even test it. Error: {str(e)}")

    @bot.command(name='correlation', help="Calculate Pearson correlation coefficient. Usage: !correlation [x1,x2,...] [y1,y2,...]")
    async def correlation(ctx, x_data: str, y_data: str):
        try:
            x = [safe_float_conversion(x) for x in x_data.split(',')]
            y = [safe_float_conversion(y) for y in y_data.split(',')]
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Can't correlate apples with oranges, you know?")
            
            r, p = stats.pearsonr(x, y)
            result = f"Pearson correlation coefficient: {r:.4f}\nP-value: {p:.4f}"
            conclusion = "significant correlation" if p < 0.05 else "no significant correlation"
            
            response = maho_response("Pearson correlation", result, conclusion)
            
            fig = plot_3b1b_scatter(x, y, "Correlation Scatter Plot")
            ax = fig.gca()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'correlation_plot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error calculating correlation: {str(e)}. Did you forget how to input data correctly?")

    @bot.command(name='regression', help="Perform simple linear regression. Usage: !regression [x1,x2,...] [y1,y2,...]")
    async def regression(ctx, x_data: str, y_data: str):
        try:
            x = np.array([safe_float_conversion(x) for x in x_data.split(',')])
            y = np.array([safe_float_conversion(y) for y in y_data.split(',')])
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Are you trying to confuse me?")
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            result = f"Slope: {slope:.4f}\nIntercept: {intercept:.4f}\n"
            result += f"R-squared: {r_value**2:.4f}\np-value: {p_value:.4f}"
            conclusion = "significant relationship" if p_value < 0.05 else "no significant relationship"
            
            response = maho_response("Linear regression", result, conclusion)
            
            setup_3b1b_style()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x, y, color='#FFB26B', alpha=0.7)
            ax.plot(x, intercept + slope*x, color='#FF7B54', label='Regression line')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Linear Regression (try to follow the line)', fontsize=16, pad=20)
            ax.legend()
            
            buf = save_plot_as_bytes(fig)
            await ctx.send(response, file=discord.File(buf, 'regression_plot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error performing regression: {str(e)}. Maybe stick to drawing lines by hand?")

    @bot.command(name='mannwhitney', help="Mann-Whitney U test. Usage: !mannwhitney [data1] | [data2]")
    async def mann_whitney_test(ctx, *, data: str):
        try:
            group1, group2 = [list(map(safe_float_conversion, group.split())) for group in data.split('|')]
            if len(group1) < 2 or len(group2) < 2:
                raise commands.BadArgument("Each group must have at least two values.")
            
            statistic, p_value = stats.mannwhitneyu(group1, group2)

            result = f"U-statistic: {statistic:.4f}\nP-value: {p_value:.4f}"
            conclusion = "reject" if p_value < 0.05 else "fail to reject"
            response = maho_response("Mann-Whitney U test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            raise commands.BadArgument(f"Are you trying to confuse me? Your data is invalid. Error: {str(e)}")

    @bot.command(name='pearson', help="Calculate Pearson correlation coefficient. Usage: !pearson [x1,x2,...] [y1,y2,...]")
    async def pearson_correlation(ctx, x_data: str, y_data: str):
        try:
            x = [safe_float_conversion(x) for x in x_data.split(',')]
            y = [safe_float_conversion(y) for y in y_data.split(',')]
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Are you trying to correlate apples and oranges?")
            r, p = stats.pearsonr(x, y)
            result = f"Pearson correlation coefficient: {r:.4f}\np-value: {p:.4f}"
            conclusion = "significant correlation" if p < 0.05 else "no significant correlation"
            response = maho_response("Pearson correlation", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error calculating correlation: {str(e)}. Did you forget how to input data correctly?")

    @bot.command(name='spearman', help="Calculate Spearman rank correlation. Usage: !spearman [x1,x2,...] [y1,y2,...]")
    async def spearman_correlation(ctx, x_data: str, y_data: str):
        try:
            x = [safe_float_conversion(x) for x in x_data.split(',')]
            y = [safe_float_conversion(y) for y in y_data.split(',')]
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Did you lose count somewhere?")
            r, p = stats.spearmanr(x, y)
            result = f"Spearman rank correlation coefficient: {r:.4f}\np-value: {p:.4f}"
            conclusion = "significant correlation" if p < 0.05 else "no significant correlation"
            response = maho_response("Spearman correlation", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error calculating Spearman correlation: {str(e)}. Maybe stick to simpler statistics?")

    @bot.command(name='wilcoxon', help="Perform Wilcoxon signed-rank test. Usage: !wilcoxon [x1,x2,...] [y1,y2,...]")
    async def wilcoxon_test(ctx, x_data: str, y_data: str):
        try:
            x = [safe_float_conversion(x) for x in x_data.split(',')]
            y = [safe_float_conversion(y) for y in y_data.split(',')]
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Did you miscount?")
            statistic, p = stats.wilcoxon(x, y)
            result = f"Wilcoxon signed-rank test statistic: {statistic:.4f}\np-value: {p:.4f}"
            conclusion = "reject" if p < 0.05 else "fail to reject"
            response = maho_response("Wilcoxon signed-rank test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error performing Wilcoxon test: {str(e)}. Maybe you should review your basic statistics?")

    @bot.command(name='kruskal', help="Perform Kruskal-Wallis H-test. Usage: !kruskal [group1: x1,x2,...] [group2: y1,y2,...] ...")
    async def kruskal_wallis_test(ctx, *args):
        try:
            groups = [[safe_float_conversion(x) for x in group.split(':')[1].split(',')] for group in args]
            if len(groups) < 2:
                raise ValueError("At least two groups are required. Can't compare a group to itself, you know?")
            statistic, p = stats.kruskal(*groups)
            result = f"Kruskal-Wallis H-test statistic: {statistic:.4f}\np-value: {p:.4f}"
            conclusion = "reject" if p < 0.05 else "fail to reject"
            response = maho_response("Kruskal-Wallis H-test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error performing Kruskal-Wallis test: {str(e)}. Are you sure you know what you're doing?")

    @bot.command(name='friedman', help="Perform Friedman test. Usage: !friedman [subject1: x1,y1,z1,...] [subject2: x2,y2,z2,...] ...")
    async def friedman_test(ctx, *args):
        try:
            data = [list(map(safe_float_conversion, subject.split(':')[1].split(','))) for subject in args]
            if len(data) < 2:
                raise ValueError("At least two subjects are required. One subject isn't much of an experiment, is it?")
            statistic, p = stats.friedmanchisquare(*zip(*data))
            result = f"Friedman test statistic: {statistic:.4f}\np-value: {p:.4f}"
            conclusion = "reject" if p < 0.05 else "fail to reject"
            response = maho_response("Friedman test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error performing Friedman test: {str(e)}. Maybe leave the complex stats to the professionals?")

    @bot.command(name='levene', help="Perform Levene's test for equality of variances. Usage: !levene [group1: x1,x2,...] [group2: y1,y2,...] ...")
    async def levene_test(ctx, *args):
        try:
            groups = [[safe_float_conversion(x) for x in group.split(':')[1].split(',')] for group in args]
            if len(groups) < 2:
                raise ValueError("At least two groups are required. Can't compare a group to itself, genius.")
            statistic, p = stats.levene(*groups)
            result = f"Levene's test statistic: {statistic:.4f}\np-value: {p:.4f}"
            conclusion = "reject" if p < 0.05 else "fail to reject"
            response = maho_response("Levene's test", result, conclusion)
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error performing Levene's test: {str(e)}. Did you even read the usage instructions?")

    @bot.command(name='latex', help="Render a LaTeX equation. Usage: !latex [equation]")
    async def render_latex(ctx, *, equation: str):
        try:
            # URL encode the LaTeX equation
            encoded_equation = urllib.parse.quote(equation)
            
            # Construct the URL for the CodeCogs LaTeX renderer
            latex_url = f"https://latex.codecogs.com/png.latex?\\dpi{{300}}\\bg_white\\large%20{encoded_equation}"
            
            # Create an embed with the image
            embed = discord.Embed()
            embed.set_image(url=latex_url)
            
            response = f"Here's your equation, try not to get a headache:"
            await ctx.send(response, embed=embed)
        except Exception as e:
            raise commands.BadArgument(f"Ugh, your LaTeX is so bad even I can't render it. Error: {str(e)}")

    @bot.command(name='histogram', help="Create a histogram. Usage: !histogram [data1,data2,...]")
    async def histogram(ctx, data: str):
        try:
            values = [safe_float_conversion(x) for x in data.split(',')]
            fig = plot_3b1b_histogram(values, "Histogram of Data")
            buf = save_plot_as_bytes(fig)
            await ctx.send("Here's your histogram. Try not to hurt yourself interpreting it.", 
                           file=discord.File(buf, 'histogram.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error creating histogram: {str(e)}. Did you forget how numbers work?")

    @bot.command(name='boxplot', help="Create a box plot. Usage: !boxplot [group1: x1,x2,...] [group2: y1,y2,...] ...")
    async def boxplot(ctx, *args):
        try:
            data = [list(map(safe_float_conversion, group.split(':')[1].split(','))) for group in args]
            labels = [group.split(':')[0] for group in args]
            fig = plot_3b1b_boxplot(data, labels, "Box Plot of Groups")
            buf = save_plot_as_bytes(fig)
            await ctx.send("Here's your box plot. Try not to get lost in the boxes.", 
                           file=discord.File(buf, 'boxplot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error creating box plot: {str(e)}. Maybe stick to simple bar graphs?")

    @bot.command(name='factorial', help="Calculate factorial. Usage: !factorial [n]")
    async def calc_factorial(ctx, n: int):
        try:
            result = factorial(n)
            response = f"The factorial of {n} is {result}. Impressed? You shouldn't be, it's basic math."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='combination', help="Calculate combinations. Usage: !combination [n] [k]")
    async def calc_combination(ctx, n: int, k: int):
        try:
            result = combination(n, k)
            response = f"The number of ways to choose {k} items from {n} items is {result}. Don't ask me to list them all."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='permutation', help="Calculate permutations. Usage: !permutation [n] [k]")
    async def calc_permutation(ctx, n: int, k: int):
        try:
            result = permutation(n, k)
            response = f"The number of ways to arrange {k} items from {n} items is {result}. Good luck listing all of those."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='binomial', help="Calculate binomial probability. Usage: !binomial [n] [k] [p]")
    async def calc_binomial(ctx, n: int, k: int, p: float):
        try:
            result = binomial_probability(n, k, p)
            response = f"The probability of {k} successes in {n} trials with p={p} is {result:.6f}. Don't bet on it though."
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='poisson', help="Calculate Poisson probability. Usage: !poisson [k] [lambda]")
    async def calc_poisson(ctx, k: int, lambda_: float):
        try:
            result = poisson_probability(k, lambda_)
            response = f"The Poisson probability of {k} events with lambda={lambda_} is {result:.6f}. Feeling random yet?"
            await ctx.send(response)
        except ValueError as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.command(name='coin_flip', help="Simulate coin flips. Usage: !coin_flip [number of flips]")
    async def coin_flip(ctx, n: int):
        if n <= 0 or n > 1000000:
            await ctx.send("Number of flips must be between 1 and 1,000,000. I don't have all day, you know.")
            return
        
        flips = np.random.choice(['H', 'T'], size=n)
        heads = np.sum(flips == 'H')
        tails = n - heads
        
        response = f"Out of {n} coin flips:\n"
        response += f"Heads: {heads} ({heads/n:.2%})\n"
        response += f"Tails: {tails} ({tails/n:.2%})\n"
        response += "What, did you expect it to be exactly 50-50? Welcome to real probability."
        
        await ctx.send(response)

    @bot.command(name='dice_roll', help="Simulate dice rolls. Usage: !dice_roll [number of dice] [number of sides]")
    async def dice_roll(ctx, dice: int, sides: int):
        if dice <= 0 or dice > 1000:
            await ctx.send("Number of dice must be between 1 and 1,000. I'm not a casino, you know.")
            return
        if sides < 2 or sides > 100:
            await ctx.send("Number of sides must be between 2 and 100. What kind of weird dice are you using?")
            return
        
        rolls = np.random.randint(1, sides + 1, size=dice)
        total = np.sum(rolls)
        
        response = f"Rolling {dice} {sides}-sided dice:\n"
        response += f"Individual rolls: {', '.join(map(str, rolls))}\n"
        response += f"Total: {total}\n"
        response += f"Average roll: {total/dice:.2f}\n"
        response += "Don't blame me if you didn't get the number you wanted."
        
        await ctx.send(response)

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
