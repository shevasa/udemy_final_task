from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

no_ref_callback = CallbackData("start_no_ref", "action")

no_refferal_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="✍🏾Ввести код приглашения",
                             callback_data=no_ref_callback.new(action="enter_invitation_code"))
    ],
    [
        InlineKeyboardButton(text="✅Проверить подписку на канал",
                             callback_data=no_ref_callback.new(action="check_subscription"))
    ]
])