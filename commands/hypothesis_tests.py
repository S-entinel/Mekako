# commands/hypothesis_tests.py
import discord
from discord.ext import commands
from ..utils.calculations import safe_float_conversion, validate_positive
from ..utils.plotting import *
from ..personality.responses import maho_response
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def hypothesis_tests_setup(bot):
    @bot.command(name='ttest', help="One-sample t-test. Usage: !ttest [sample_mean] [population_mean] [sample_std] [sample_size]")
    async def t_test(ctx, sample_mean: float, population_mean: float, sample_std: float, sample_size: int):
        try:
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
        except Exception as e:
            await ctx.send(f"Error performing t-test: {str(e)}. Did you skip Statistics 101?")


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