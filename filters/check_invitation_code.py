import logging

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class Check_user_id(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        try:
            id_to_check = int(message.text)
        except ValueError as err:
            logging.error(err)
            await message.answer("❌Неправильно введен код!❌\nПопробуйте войти еще раз!")
            return False
        check_user = await db.get_user_by_user_id(id_to_check)
        if check_user:
            await message.answer("✅Код правильный!✅")
            return True
        else:
            await message.answer("❌Неверный код!❌\nПопробуйте войти еще раз!")
            return False

