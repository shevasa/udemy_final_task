from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class Check_old_user(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user = await db.get_user_by_user_id(message.from_user.id)
        if user:
            return True
        else:
            return False