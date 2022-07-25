import discord
from discord.ext.commands import Bot
from sqlalchemy.orm import Session

from config import DiscordServer


class BaseDiscordOperator:
    """Класс с базовыми операциями с дискордом"""

    def __init__(self, bot: Bot, config: DiscordServer, pg_connection: Session):
        self._bot = bot
        self._config = config
        self._pg = pg_connection

    async def send_msg(
            self, chat_id: int,
            msg: str | discord.Embed
    ):
        """Отправка сообщения в указанный чат"""

        channel: discord.TextChannel | discord.DMChannel
        channel = self._bot.get_channel(chat_id)

        if not isinstance(channel, (discord.TextChannel, discord.DMChannel)):
            raise ValueError(
                f'Чат не обнаружен или не является текстовым ({type(channel)})')

        if isinstance(msg, discord.Embed):
            await channel.send(embed=msg)
        else:
            await channel.send(msg)
