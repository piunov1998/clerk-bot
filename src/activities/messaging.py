import discord
from discord.ext import commands
from config import DiscordServer


class Messaging:
    """Класс для отправки осмысленных сообщений"""

    def __init__(self, bot: commands.Bot, cfg: DiscordServer):
        self.bot = bot
        self.config = cfg

    async def announce(self, msg: str):
        """Объявление"""

        channel: discord.TextChannel = self.bot.get_channel(
            self.config.info_channel
        )
        await channel.send(msg)
