from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import Check_old_user
from loader import dp, db, bot


@dp.inline_handler(Check_old_user())
async def some_query(query: types.InlineQuery):
    products = await db.get_needed_products(query.query)
    results = []
    bot_username = (await bot.me).username
    for num, product in enumerate(products, start=1):
        product = dict(product)
        results.append(types.InlineQueryResultPhoto(id=f'{num}', photo_url=product.get('photo_url'),
                                                    thumb_url=product.get('photo_url'),
                                                    photo_height=512,
                                                    photo_width=512,
                                                    title=product.get('name'),
                                                    caption=f"\nЦена: {product.get('price')}UAH",
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text="👀Показать товар",
                                                                                 url=f"https://t.me/{bot_username}?start={product.get('product_id')}",
                                                                                 callback_data=f"{product.get('product_id')}")

                                                        ]
                                                    ])
                                                    ))
    await query.answer(results=results)
