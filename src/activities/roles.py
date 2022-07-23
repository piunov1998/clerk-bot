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
                    'id': role.id,
                    'name': role.name
                })
        return roles

