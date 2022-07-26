import discord
from discord import Guild

from .base import BaseDiscordOperator


class Roles(BaseDiscordOperator):
    """Управление ролями"""

    def get_roles(self):
        """Получить роли на сервере"""

        guild: Guild = self._bot.get_guild(self._config.guild_id)
        roles = []
        for role in guild.roles:
            if role.hoist:
                roles.append({
                    'id': str(role.id),
                    'name': role.name
                })
        return roles

    def get_role(self, role_id: int) -> discord.Role:
        """Получить роль по id"""

        guild: Guild = self._bot.get_guild(self._config.guild_id)
        for role in guild.roles:
            if role.id == role_id:
                return role
