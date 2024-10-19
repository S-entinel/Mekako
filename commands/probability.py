# commands/probability.py
import discord
from discord.ext import commands
from ..utils.calculations import factorial, combination, permutation, binomial_probability, poisson_probability
from ..personality.responses import maho_response
import numpy as np

def probability_setup(bot):
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

    # Add other probability commands here...