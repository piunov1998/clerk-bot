from discord.ext.commands import Bot

from config import config
from activities import Messaging, Roles, Registration
from .connections import acquire_session


class ActivitiesInj:
    """Инъектор для действий"""

    def __init__(self, bot: Bot):
        self._bot = bot

    def messaging(self) -> Messaging:
        return Messaging(
            bot=self._bot,
            config=config.discord.server_info,
            pg_connection=acquire_session()
        )

    def roles(self) -> Roles:
        return Roles(
            bot=self._bot,
            config=config.discord.server_info,
            pg_connection=acquire_session()
        )

    def registration(self) -> Registration:
        return Registration(
            bot=self._bot,
            config=config.discord.server_info,
            pg_connection=acquire_session()
        )
