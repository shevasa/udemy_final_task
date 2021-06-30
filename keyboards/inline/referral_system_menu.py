from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

referral_system_callback = CallbackData('referral_system', 'action')

referral_system_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показать реферралов👦👩",
                             callback_data=referral_system_callback.new(action='show_referrals'))
    ],
    [
        InlineKeyboardButton(text='🔙Назад', callback_data=referral_system_callback.new(action='exit_to_start'))
    ]
])
