import enum

from pydantic import BaseModel


class CommandsTypes(enum.Enum):
    """Типы команд"""

    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class InteractionTypes(enum.Enum):
    """Типы взаимодействий"""

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 54
    MODAL_SUBMIT = 5


class InteractionData(BaseModel):
    """Данные взаимодействия"""

    id: int
    name: str
    type: CommandsTypes
    options: list[dict]
    guild_id: int
    target_id: int


class User(BaseModel):
    """Модель юзера"""

    id: int


class Member(BaseModel):
    """Модель члена сервера"""

    user: User


class Interaction(BaseModel):
    """Модель interaction слеш-команд"""

    id: int
    application_id: int
    type: InteractionTypes
    guild_id: int | None
    channel_id: int | None
    member: Member | None
    user: User | None
    token: str
