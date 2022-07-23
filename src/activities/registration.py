import random

import discord
from discord import Embed

from .base import BaseDiscordOperator


class Registration(BaseDiscordOperator):
    """Управление регистрацией"""

    async def registration(self, data: dict):
        """Обработка персональных данных"""

        admins: list[discord.User]
        admins = [self._bot.get_user(id_) for id_ in self._config.admins_ids]

        embed = Embed()
        embed.title = f'**Заявка на вступление №{random.randint(0, 9999):0>4}**'
        blank = f'**Фамилия**: {data.get("lastname")}\n' \
                f'**Имя**: {data.get("firstname")}\n' \
                f'**Очество**: {data.get("middlename")}\n' \
                f'**Возраст**: {data.get("age")}\n' \
                f'**Желаемое прозвище**: {data.get("wonder_nick")}\n' \
                f'**Желаемая роль**: {data.get("wonder_role")}'

        embed.description = blank
        embed.colour = discord.Color.blue()

        for admin in admins:
            if admin.dm_channel is None:
                chat: discord.DMChannel = await admin.create_dm()
            else:
                chat: discord.DMChannel = admin.dm_channel
            print(admin.name, admin.dm_channel)
            await self.send_msg(chat.id, embed)
