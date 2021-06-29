import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp, db, bot
from utils.misc.product_class import Product


@dp.message_handler(CommandStart(re.compile(r'\d{1,4}')))
async def show_product(message: types.Message):
    product_id = int(message.get_args())
    chosen_product = await db.get_specific_product(product_id)
    prices = [types.LabeledPrice(label=f'{chosen_product.get("name")}', amount=chosen_product.get("price") * 100)]
    product_in_invoice = Product(title=f'{chosen_product.get("name")}', currency="UAH", prices=prices,
                                 description=chosen_product.get("description"),
                                 start_parameter='selling',
                                 photo_url=chosen_product.get('photo_url'),
                                 photo_height=512, photo_width=512)
    await bot.send_invoice(chat_id=message.chat.id, payload=f'{chosen_product.get("product_id")}000',
                           **product_in_invoice.generate_invoice())


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
