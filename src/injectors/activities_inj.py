from discord.ext.commands import Bot

from config import config
from activities import Messaging, Roles, Registration


class ActivitiesInj:
    """Инъектор для действий"""

    def __init__(self, bot: Bot):
        self._bot = bot

    def messaging(self) -> Messaging:
        return Messaging(self._bot, config.discord.server_info)

    def roles(self) -> Roles:
        return Roles(self._bot, config.discord.server_info)

    def registration(self) -> Registration:
        return Registration(self._bot, config.discord.server_info)
