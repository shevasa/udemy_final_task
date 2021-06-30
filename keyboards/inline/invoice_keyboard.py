from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

invoice_callback = CallbackData('invoice', 'action')


invoice_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Расчитаться бонусами', callback_data=invoice_callback.new(action='pay_by_bonus'))
    ]
])