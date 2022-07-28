from .base import BaseDiscordOperator
from models import Credits


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
