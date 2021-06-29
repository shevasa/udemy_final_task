from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

admin_panel_callback = CallbackData('admin_panel', 'action')

admin_panel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='➕Добавить товар', callback_data=admin_panel_callback.new(action='add_product'))
    ],
    [
        InlineKeyboardButton(text='🔙Назад', callback_data=admin_panel_callback.new(action='exit_to_start'))
    ]
])