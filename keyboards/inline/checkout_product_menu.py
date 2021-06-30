from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

checkout_callback = CallbackData('checkout_product', 'action', 'product_id', 'quantity')


async def get_checkout_menu(product_id: int, only_card: bool = False, quantity: int = 1):
    checkout_menu = InlineKeyboardMarkup(row_width=1)

    if not only_card:
        quantity_button = InlineKeyboardButton(text=f'🖐🏾Количество товара - {quantity}',
                                               callback_data=checkout_callback.new(action='choose_quantity',
                                                                                   product_id=product_id,
                                                                                   quantity=quantity))
        bonus_pay_button = InlineKeyboardButton(text='Оплатить бонусами💎',
                                                callback_data=checkout_callback.new(action='pay_by_bonus',
                                                                                    product_id=product_id,
                                                                                    quantity=quantity
                                                                                    ))
        checkout_menu.add(quantity_button, bonus_pay_button)

    card_pay_button = InlineKeyboardButton(text='Оплатить картой💳',
                                           callback_data=checkout_callback.new(action='pay_by_card',
                                                                               product_id=product_id,
                                                                               quantity=quantity
                                                                               ))
    checkout_menu.add(card_pay_button)

    return checkout_menu
