from models import Credits
from .base import BaseDiscordOperator


class CreditsService(BaseDiscordOperator):
    """Класс управления социальными кредитами"""

    def get_credits(self, user_id: int) -> int:
        """Получить количество кредитов"""

        credits_account: Credits = self._pg.get(Credits, user_id)
        if credits_account is None:
            credits_account = Credits(user_id, 500)
            with self._pg.begin():
                self._pg.add(credits_account)
        return credits_account.total

    def spend_credits(self, user_id: int, value: int, reason: str) -> int:
        """Потратить кредиты"""

        with self._pg.begin():
            credits_account: Credits = self._pg.get(Credits, user_id)
            credits_account.total -= value

        return credits_account.total
