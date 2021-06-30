import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline import checkout_callback, get_checkout_menu
from loader import dp, db, bot
from utils.misc.product_class import Product


@dp.message_handler(state='quantity_chosen')
@dp.message_handler(CommandStart(re.compile(r'\d{1,4}')))
async def show_product(message: types.Message, state: FSMContext):
    if await state.get_state():
        product_id = (await state.get_data()).get('product_id')
        try:
            quantity = int(message.text)
            if 15 <= quantity:
                await message.answer('❗️Количество должно быть от 1 до 15 единиц❗️')
                quantity = (await state.get_data()).get('quantity')
        except ValueError:
            await message.answer('❗️Неправильно указано количество❗️')
            quantity = (await state.get_data()).get('quantity')
        await state.reset_state()
    else:
        product_id = int(message.get_args())
        quantity = 1
    chosen_product = await db.get_specific_product(product_id)
    caption = f"Название: {chosen_product.get('name')}\n\n" + f"Описание: {chosen_product.get('description')}\n\n" + \
              f"Цена: {int(chosen_product.get('price')) * quantity}UAH\n\n" + f"Количество: {quantity}"
    await message.answer_photo(photo=chosen_product.get('photo_url'), caption=caption,
                               reply_markup=await get_checkout_menu(product_id=product_id, quantity=quantity))


@dp.callback_query_handler(checkout_callback.filter(action='choose_quantity'))
async def choose_quantity(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите нужное количество (От 1 до 15)')
    await state.set_state("quantity_chosen")
    await state.update_data({
        "product_id": int(call.data.split(':')[2]),
        "quantity": int(call.data.split(':')[3])
    })


@dp.callback_query_handler(checkout_callback.filter(action='pay_by_bonus'))
async def pay_by_bonus(call: types.CallbackQuery):
    product_id = int(call.data.split(':')[2])
    quantity = int(call.data.split(':')[3])
    bonus = int(dict(await db.get_user_by_user_id(call.from_user.id)).get('money'))
    chosen_product_price = int(dict(await db.get_specific_product(product_id)).get('price'))
    if bonus >= chosen_product_price * quantity:
        await db.pay_by_bonus(chosen_product_price * quantity, call.from_user.id)
        await call.message.answer(
            ' 🎆Вы успешно оплатили товар бонусами🎆\n\n'
            'Наши операторы свяжуться с вами в скором времени для уточнения условий доставки!'
            f'Хорошего дня!\nНа вашем бонусном счету: {bonus - chosen_product_price * quantity}UAH'
            '\n\nНажмите /start чтобы перейти в главное меню')
    else:
        await call.message.answer('❌Недостаточно средств на счету❌\n\n'
                                  f'На вашем бонусном счету: {bonus}UAH\n'
                                  f'Стоимость выбраного товара: {chosen_product_price * quantity}UAH\n\n'
                                  'Перейти в главное меню: /start',
                                  reply_markup=await get_checkout_menu(product_id=product_id, only_card=True,
                                                                       quantity=quantity))


@dp.callback_query_handler(checkout_callback.filter(action='pay_by_card'))
async def send_invoice(call: types.CallbackQuery):
    product_id = int(call.data.split(':')[2])
    quantity = int(call.data.split(':')[3])
    chosen_product = await db.get_specific_product(product_id)
    prices = [
        types.LabeledPrice(label=f'{chosen_product.get("name")}', amount=chosen_product.get("price") * quantity * 100)]
    product_in_invoice = Product(title=f'{chosen_product.get("name")}', currency="UAH", prices=prices,
                                 description=chosen_product.get("description") + f"\nКоличество: {quantity}",
                                 start_parameter='selling',
                                 photo_url=chosen_product.get('photo_url'),
                                 photo_height=512, photo_width=512)
    await bot.send_invoice(chat_id=call.message.chat.id, payload=f'{chosen_product.get("product_id")}000',
                           **product_in_invoice.generate_invoice())


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
