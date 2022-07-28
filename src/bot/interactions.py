import json
import logging

import aiohttp
import discord
from discord.ext.commands import Bot

from injectors import ActivitiesInj
from config import DiscordConfig
from models.interactions import Interaction, InteractionTypes, CommandsTypes


class InteractionsProcessor:
    """Класс для обработки слеш-комманд"""

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

    async def set_up_commands(self):
        url = f'{self._base_url}/applications/{self._config.application_id}/' \
              f'guilds/{self._config.guild_info.guild_id}/commands'
        data = {
            'name': 'credits',
            'type': 1,
            'description': 'Текущий баланс социальных кредитов'
        }
        async with self._session.post(
                url=url,
                data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        ) as resp:
            logging.info(await resp.json())

    async def on_interaction(self, interaction: Interaction):
        id_ = interaction.id
        token = interaction.token
        total = self._act.credits_service().get_credits(
            interaction.member.user.id
        )

        resp = {
            'type': 4,
            'data': {
                'content': f'На вашем счету **{total:,}** социальных кредитов'
            }
        }
        await self.interaction_response(id_, token, resp)

    async def interaction_response(
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
