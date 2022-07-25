import random
import string
from datetime import datetime
from hashlib import md5

import discord
import sqlalchemy as sa
from discord import Embed

from models import Request, RequestDataValidator, User
from .base import BaseDiscordOperator


class Registration(BaseDiscordOperator):
    """Управление регистрацией"""

    @classmethod
    def generate_password(cls) -> str:
        """Генерация пароля"""

        abc = string.digits + string.ascii_letters
        return ''.join([random.choice(abc) for _ in range(8)])

    def add_user(self, user_id: int) -> User:
        """Создание пользователя"""

        user: discord.User = self._bot.get_user(user_id)
        user = User(
            id=user.id,
            nickname=user.name,
            login=user.display_name,
            password=md5(bytes(self.generate_password(), 'utf-8')).hexdigest()
        )
        with self._pg.begin():
            self._pg.add(user)
        return user

    def create_request(self, user_id: int) -> Request:
        """Создание заявки"""

        request = Request(
            user=user_id,
            data=None,
            date=datetime.now()
        )
        with self._pg.begin():
            self._pg.add(request)
        return request

    def get_request(
            self,
            *,
            user_id: int = None,
            request_id: int = None
    ) -> Request:
        """Получить заявку по id или id пользователя"""

        if user_id is None and request_id is None or \
                user_id is not None and request_id is not None:
            raise AttributeError('Должен быть укзаан лишь один из параметров')

        if request_id is not None:
            return self._pg.get(Request, request_id)
        else:
            return self._pg.execute(
                sa.select(Request).filter(Request.user == user_id)
            ).scalar_one_or_none()

    def update_request(
            self,
            request: Request,
            data: RequestDataValidator
    ) -> Request:
        """Изменение заявки"""

        with self._pg.begin():
            request.data = data
        return request

    async def registration(self, user_id: int, data: RequestDataValidator):
        """Обработка персональных данных"""

        admins: list[discord.User]
        admins = [self._bot.get_user(id_) for id_ in self._config.admins_ids]

        request = self.get_request(user_id=user_id)
        user: discord.User = self._bot.get_user(user_id)
        with self._pg.begin():
            request.data = data.dict()

        embed = Embed()
        birth_date = datetime.fromtimestamp(data.birth_date / 1000).isoformat()
        embed.title = f'**Заявка на вступление №{request.id:0>4}**'
        blank = \
            f'**Пользователь**: {user.display_name}#{user.discriminator}\n' \
            f'**Фамилия**: {data.lastname}\n' \
            f'**Имя**: {data.firstname}\n' \
            f'**Отчество**: {data.middlename}\n' \
            f'**Дата рождения**: {birth_date}\n' \
            f'**Пол**: {data.sex}\n' \
            f'**Национальность**: {data.nation}\n' \
            f'**Вероисповедание**: {data.religion}\n' \
            f'**Желаемое прозвище**: {data.wonder_nick}\n' \
            f'**Желаемая должность**: {data.wonder_role}'

        embed.description = blank
        embed.colour = discord.Color.blue()

        for admin in admins:
            if admin.dm_channel is None:
                chat: discord.DMChannel = await admin.create_dm()
            else:
                chat: discord.DMChannel = admin.dm_channel
            await self.send_msg(chat.id, embed)
