# commands/basic_stats.py
import discord
from discord.ext import commands
from ..utils.calculations import safe_float_conversion
from ..utils.plotting import plot_3b1b_histogram, save_plot_as_bytes
from ..personality.responses import maho_response
import numpy as np

def basic_stats_setup(bot):
    @bot.command(name='histogram', help="Create a histogram. Usage: !histogram [data1,data2,...]")
    async def histogram(ctx, data: str):
        try:
            values = [safe_float_conversion(x) for x in data.split(',')]
            fig = plot_3b1b_histogram(values, "Histogram of Data")
            buf = save_plot_as_bytes(fig)
            
            await ctx.send("Here's your histogram. Try not to hurt yourself interpreting it.", 
                           file=discord.File(buf, 'histogram.png'))
        except Exception as e:
            await ctx.send(f"Error creating histogram: {str(e)}. Did you forget how numbers work?")

    @bot.command(name='mean', help="Calculate the mean. Usage: !mean [data1,data2,...]")
    async def calc_mean(ctx, data: str):
        try:
            values = [safe_float_conversion(x) for x in data.split(',')]
            result = np.mean(values)
            response = f"The mean is {result:.4f}. Impressed? You shouldn't be, it's just addition and division."
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error calculating mean: {str(e)}. Did you forget how to input numbers?")

    @bot.command(name='median', help="Calculate the median. Usage: !median [data1,data2,...]")
    async def calc_median(ctx, data: str):
        try:
            values = [safe_float_conversion(x) for x in data.split(',')]
            result = np.median(values)
            response = f"The median is {result:.4f}. It's the middle value, in case you didn't know."
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error calculating median: {str(e)}. Is sorting too complex for you?")

    # Add more basic stats commands as needed