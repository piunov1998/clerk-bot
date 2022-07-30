import enum
import typing as t
from typing import Callable, Any, Coroutine

from pydantic import BaseModel, validator


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


class OptionChoice(BaseModel):
    name: str
    value: Any


class Choices:

    def __init__(self, choices: list[OptionChoice]):
        self._choices = choices

    def __getitem__(self, item):
        for choice in self._choices:
            if choice.name == item:
                return choice

    @classmethod
    def __get_validators__(cls):
        return []


class CommandOption(BaseModel):
    """Модель опции команд"""

    type: int
    name: str
    value: Any | None
    description: str | None
    options: dict | None
    choices: Choices | None

    @validator('choices')
    def validate_choices(cls, value):
        return Choices(value)


class Options:

    def __init__(self, options: list[dict]):
        self._options = [CommandOption(**opt) for opt in options]

    def __getitem__(self, item):
        for opt in self._options:
            if opt.name == item:
                return opt

    @classmethod
    def __get_validators__(cls):
        return []


class InteractionData(BaseModel):
    """Данные взаимодействия"""

    id: int
    name: str
    type: CommandsTypes
    options: Options | None
    guild_id: int | None
    target_id: int | None

    @validator('options')
    def validate_options(cls, value):
        return Options(value)


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
    data: InteractionData


class SlashCommands:

    def __init__(self):
        self._commands: dict[str, t.Callable[[Interaction], dict]] = {}

    @property
    def commands(self) -> list[str]:
        return [cmd for cmd in self._commands]

    def __getitem__(self, item):
        return self._commands[item]

    def command(self, name: str = None) -> t.Callable:
        def decorator(
                command: t.Callable[[Interaction], t.Awaitable[dict]]
        ) -> Callable[[Interaction], Coroutine[Any, Any, dict]]:
            self._commands.update({name or command.__name__: command})

            async def wrapper(interaction: Interaction):
                return await command(interaction)

            return wrapper

        return decorator
