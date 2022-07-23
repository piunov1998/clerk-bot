from discord.ext import commands

from config import config

config = config.discord

bot = commands.Bot(command_prefix=config.prefix)
