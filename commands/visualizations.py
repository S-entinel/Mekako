# commands/visualizations.py
import discord
from discord.ext import commands
from ..utils.calculations import safe_float_conversion
from ..utils.plotting import *
import matplotlib.pyplot as plt
from ..personality.responses import maho_response
from scipy import stats

def visualizations_setup(bot):
    @bot.command(name='scatter', help="Create a scatter plot. Usage: !scatter [x1,x2,...] [y1,y2,...]")
    async def scatter_plot(ctx, x_data: str, y_data: str):
        try:
            x = [safe_float_conversion(x) for x in x_data.split(',')]
            y = [safe_float_conversion(y) for y in y_data.split(',')]
            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of elements. Can't you count?")
            
            fig = plot_3b1b_scatter(x, y, "Scatter Plot")
            buf = save_plot_as_bytes(fig)
            await ctx.send("Here's your scatter plot. Try not to get lost in the dots.", 
                           file=discord.File(buf, 'scatter_plot.png'))
            plt.close(fig)
        except Exception as e:
            await ctx.send(f"Error creating scatter plot: {str(e)}. Did you forget how to input data correctly?")

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

    # Add other visualization commands here...