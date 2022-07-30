import json
import logging

import aiohttp
from discord.ext.commands import Bot

from config import DiscordConfig
from injectors import ActivitiesInj
from models.interactions import (
    Interaction,
    SlashCommands
)


class InteractionsProcessor:
    """Класс для обработки слеш-комманд"""

    slash = SlashCommands()

    def __init__(
            self,
            bot: Bot,
            activities: ActivitiesInj,
            config: DiscordConfig
    ):
        self._act = activities
        self._bot = bot
        self._config = config
        self._session = aiohttp.ClientSession(
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bot {config.token}'
            }
        )
        self._base_url = config.api_url

    @slash.command(name='credits')
    async def get_credits(self, interaction: Interaction):
        total = self._act.credits_service().get_credits(
            interaction.member.user.id
        )

        resp = {
            'type': 4,
            'data': {
                'content': f'На вашем счету **{total:,}** социальных кредитов'
            }
        }
        return resp

    @slash.command(name='change_nick')
    async def change_nick(self, interaction: Interaction):

        cost = 1000

        if self._act.credits_service().get_credits(
                interaction.member.user.id
        ) < cost:
            return {
                'type': 4,
                'data': {
                    'content': 'Недостаточно социальных кредитов'
                }
            }

        await self._act.roles().change_nickname(
            user_id=interaction.member.user.id,
            nick=f'Товарищ {interaction.data.options["прозвище"].value}'
        )
        sc = self._act.credits_service().spend_credits(
            user_id=interaction.member.user.id,
            value=cost,
            reason='Смена прозвища'
        )
        return {
            'type': 4,
            'data': {
                'content': f'Заявка была автоматически рассмотрена. '
                           f'Прозвище было изменено, с вашего счета списано '
                           f'**1000** социальных кредитов, остаток — **{sc}**.'
            }
        }

    async def set_up_commands(self):
        url = f'{self._base_url}/applications/{self._config.application_id}/' \
              f'guilds/{self._config.guild_info.guild_id}/commands'

        commands: list[dict] = [
            {
                'name': 'credits',
                'type': 1,
                'description': 'Текущий баланс социальных кредитов'
            },
            {
                'name': 'change_nick',
                'type': 1,
                'description': 'Сменить прозвище (1000 социальных кредитов)',
                'options': [
                    {
                        'name': 'прозвище',
                        'description': 'Товарищ <прозвище>',
                        'type': 3,
                        'required': True
                    }
                ]
            }
        ]

        for data in commands:
            async with self._session.post(
                    url=url,
                    data=json.dumps(data, ensure_ascii=False).encode('utf-8')
            ) as resp:
                logging.info(await resp.json())

    async def on_interaction(self, interaction: Interaction):
        id_ = interaction.id
        token = interaction.token

        resp = await self.slash[interaction.data.name](self, interaction)

        await self.interaction_callback(id_, token, resp)

    async def interaction_callback(
            self,
            interact_id: int,
            token: str,
            data: dict
    ):
        """Формирует ответ и отправляет на сервер Discord"""

        url = f'{self._base_url}/interactions/{interact_id}/{token}/callback'
        await self._session.post(
            url=url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )

    def interaction_listener(self, interaction):
        try:
            interaction = Interaction(**interaction)
            self._bot.loop.create_task(self.on_interaction(interaction))
        except Exception as error:
            print('Error occured\n', error)
