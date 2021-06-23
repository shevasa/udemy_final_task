import logging

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import channels
from loader import bot


class Check_subscription(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        user_id = call.from_user.id
        for channel in channels:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            status_of_subscription = member.is_chat_member()
            channel = await bot.get_chat(channel)
            logging.info(f"{channel}")
            if status_of_subscription:
                await call.message.edit_text(f"✅Вы успешно подписались на канал {channel.mention}")
                return True
            else:
                await call.message.edit_text(
                    f"❌Подписка на канал не подтверждена {channel.mention}❌\n Попробуйте еще раз!")
                return False
