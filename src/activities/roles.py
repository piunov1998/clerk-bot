import logging

import discord

from models import User, Credits
from .base import BaseDiscordOperator


class Roles(BaseDiscordOperator):
    """Управление ролями"""

    def get_roles(self):
        """Получить роли на сервере"""

        guild: discord.Guild = self._bot.get_guild(self._config.guild_id)
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

        guild: discord.Guild = self._bot.get_guild(self._config.guild_id)
        for role in guild.roles:
            if role.id == role_id:
                return role

    async def change_nickname(self, user_id: int, nick: str):
        """Смена ника"""

        guild: discord.Guild = await self._bot.fetch_guild(
            guild_id=self._config.guild_id
        )
        member: discord.Member = await guild.fetch_member(user_id)
        await member.edit(reason='Сам', nick=nick)

    async def add_members_to_db(self):
        guild: discord.Guild = await self._bot.fetch_guild(
            guild_id=self._config.guild_id
        )
        member: discord.Member
        async for member in guild.fetch_members():
            if member.bot:
                continue
            user = User(
                id=member.id,
                nickname=member.nick,
                login=member.display_name,
                password=''
            )
            valet = Credits(
                user_id=member.id,
                total=500
            )
            try:
                with self._pg.begin():
                    self._pg.add(user)
                with self._pg.begin():
                    self._pg.add(valet)
            except:
                logging.warning(f'Пользователь {user.nickname} уже в базе')
