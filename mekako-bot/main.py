# main.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from commands import setup_commands
from utils import PLOT_STYLES, COLOR_MAPS, get_intent, GREETINGS, CONFUSED
import random

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        content = message.content.lower()
        intent = get_intent(content)
        
        if intent:
            response = intent.get_response(content)
            await message.channel.send(response)
        else:
            await message.channel.send(random.choice(CONFUSED))

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument? Really? Check the command usage with !help [command]. I don't have all day to explain this.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {str(error)}. Is it really that hard to enter the correct type? Check !help [command] if you're confused.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Use !help to see available commands. Don't make me repeat myself.")
    else:
        await ctx.send(f"Ugh, an error occurred: {str(error)}. Happy now?")

if __name__ == '__main__':
    setup_commands(bot)
    bot.run(os.getenv('DISCORD_TOKEN'))