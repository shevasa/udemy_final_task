from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

post_callbackdata = CallbackData("create_post", "action", "object")


async def create_post_creation_keyboard(added_name: bool = False, added_description: bool = False,
                                        added_price: bool = False,
                                        added_photo: bool = False):
    create_post_keyboard = InlineKeyboardMarkup(row_width=1)
    exit_button_text = "\U0000274CОтменить создание товара\U0000274C"

    if added_name:
        add_name_button = InlineKeyboardButton(text='Изменить название\U000021A9',
                                               callback_data=post_callbackdata.new(action='add',
                                                                                   object='name'))
    else:
        add_name_button = InlineKeyboardButton(text='Добавить название\U00002795',
                                               callback_data=post_callbackdata.new(action='add',
                                                                                   object='name'))

    if added_description:
        add_description_button = InlineKeyboardButton(text='Изменить описание\U000021A9',
                                                      callback_data=post_callbackdata.new(action='add',
                                                                                          object='description'))
    else:
        add_description_button = InlineKeyboardButton(text='Добавить описание\U00002795',
                                                      callback_data=post_callbackdata.new(action='add',
                                                                                          object='description'))

    if added_price:
        add_price_button = InlineKeyboardButton(text='Изменить цену\U000021A9',
                                                callback_data=post_callbackdata.new(action='add', object='price'))
    else:
        add_price_button = InlineKeyboardButton(text='Добавить цену\U0001F58A',
                                                callback_data=post_callbackdata.new(action='add', object='price'))

    if added_photo:
        add_photo_button = InlineKeyboardButton(text='Изменить фото\U0001F4F7',
                                                callback_data=post_callbackdata.new(action='add', object='photo'))
    else:
        add_photo_button = InlineKeyboardButton(text='Добавить фото\U0001F4F7',
                                                callback_data=post_callbackdata.new(action='add', object='photo'))

    exit_button = InlineKeyboardButton(text=exit_button_text,
                                       callback_data=post_callbackdata.new(action='exit', object='post'))
    publish_button = InlineKeyboardButton(text='Готово\U00002705',
                                          callback_data=post_callbackdata.new(action='post', object='post'))

    create_post_keyboard.add(add_name_button, add_description_button, add_price_button, add_photo_button, exit_button)
    if added_name and added_description and added_price and added_photo:
        create_post_keyboard.add(publish_button)

    return create_post_keyboard
