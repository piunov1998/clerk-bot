import discord

from .base import BaseDiscordOperator


class Messaging(BaseDiscordOperator):
    """Класс для отправки осмысленных сообщений"""

    async def announce(self, msg: str):
        """Объявление"""

        channel: discord.TextChannel = self._bot.get_channel(
            self._config.info_channel
        )
        await channel.send(msg)
