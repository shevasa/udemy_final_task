from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from typing import Union

from loader import db


class Check_old_user(BoundFilter):
    async def check(self, update: Union[types.Message, types.InlineQuery]) -> bool:
        user = await db.get_user_by_user_id(update.from_user.id)
        if user:
            return True
        else:
            return False