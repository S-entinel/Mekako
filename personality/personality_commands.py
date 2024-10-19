# commands/personality_commands.py
import discord
from discord.ext import commands
import random
from ..personality.responses import PRAISE_RESPONSES, HUG_RESPONSES

def personality_commands_setup(bot):
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
        await ctx.send(random.choice(PRAISE_RESPONSES))

    @bot.command(name='hug', help="Try to hug Mekako (at your own risk)")
    async def hug(ctx):
        await ctx.send(random.choice(HUG_RESPONSES))

