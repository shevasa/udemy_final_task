import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS

start_keyboard_callback = CallbackData("start", "move_to")


async def get_start_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_referral_button = InlineKeyboardButton(text="📢Реферальная система",
                                                 callback_data=start_keyboard_callback.new(move_to="referral_system"))
    keyboard.add(check_referral_button)
    search_button = InlineKeyboardButton(text="🔎Выбрать товар",
                                         switch_inline_query_current_chat="")
    keyboard.add(search_button)
    if str(user_id) in ADMINS:
        admin_button = InlineKeyboardButton(text="🧑🏽‍💼Админ система",
                                            callback_data=start_keyboard_callback.new(move_to="admin_system"))
        keyboard.add(admin_button)
    return keyboard
