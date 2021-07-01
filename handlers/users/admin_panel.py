from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from keyboards.inline import start_keyboard_callback, admin_panel_keyboard, admin_panel_callback
from keyboards.inline.post_creation_keyboard import create_post_creation_keyboard, post_callbackdata
from loader import dp
from states import Create_post
from utils.misc.construct_product_info import construct_info


@dp.callback_query_handler(post_callbackdata.filter(action='exit', object='post'),
                           state=Create_post.post_creation)
@dp.callback_query_handler(start_keyboard_callback.filter(move_to="admin_system"))
async def get_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if await state.get_state() == "Create_post:post_creation":
        await call.message.answer('<code>Вы отменили создание продукта</code>')
        await state.reset_state()
    await call.message.answer("<b>Панель администратора</b>", reply_markup=admin_panel_keyboard)


@dp.callback_query_handler(admin_panel_callback.filter(action='add_product'))
async def start_post_creation(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Создайте новый товар!\n\n❗️ ❕Нужно заполнить все поля ОБЯЗАТЕЛЬНО❗️ ❕",
                                 reply_markup=await create_post_creation_keyboard())
    await Create_post.post_creation.set()


@dp.callback_query_handler(post_callbackdata.filter(action='add', object='name'), state=Create_post.post_creation)
async def add_photo(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("✍🏽Отправьте название товара")
    await Create_post.add_name.set()


@dp.callback_query_handler(post_callbackdata.filter(action='add', object='description'),
                           state=Create_post.post_creation)
async def add_photo(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("✍🏽Отправьте описание товара")
    await Create_post.add_description.set()


@dp.callback_query_handler(post_callbackdata.filter(action='add', object='price'),
                           state=Create_post.post_creation)
async def add_photo(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("✍🏽Укажите цену товара")
    await Create_post.add_price.set()


@dp.callback_query_handler(post_callbackdata.filter(action='add', object='photo'),
                           state=Create_post.post_creation)
async def add_photo(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("✍🏽Отправьте ссылку на фото товара")
    await Create_post.add_photo.set()


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT],
                    state=Create_post.add_photo)
@dp.message_handler(
    state=[Create_post.add_price, Create_post.add_photo, Create_post.add_name, Create_post.add_description])
async def post_or_edit(message: types.Message, state: FSMContext):
    if await state.get_state() == "Create_post:add_price":
        try:
            price = int(message.text)
            await state.update_data(data={
                'price': price,
            })
        except ValueError:
            await message.answer('❗️Неправильно указана цена❗️')
    if await state.get_state() == "Create_post:add_photo":
        if message.content_type == types.ContentType.PHOTO or message.content_type == types.ContentType.DOCUMENT:
            await message.answer(
                "<b>Фото можно добавить только через ссылку!\nДля того чтобы в инвойсе отображалось фото продукта</b>")
        else:
            photo_url = message.text
            await state.update_data(data={
                'photo_url': photo_url
            })
    if await state.get_state() == "Create_post:add_name":
        name = message.text
        await state.update_data(data={
            'name': name
        })
    if await state.get_state() == "Create_post:add_description":
        description = message.text
        await state.update_data(data={
            'description': description
        })

    state_data = await state.get_data()
    add_to_post = await construct_info(state_data)
    photo_url = state_data.get('photo_url')
    if photo_url:
        keyboard = await create_post_creation_keyboard(added_name=bool(state_data.get('name')),
                                                       added_photo=True,
                                                       added_price=bool(state_data.get('price')),
                                                       added_description=bool(state_data.get('description')))
        try:
            await message.answer_photo(photo=photo_url, caption='\n\n'.join(add_to_post),
                                   reply_markup=keyboard)
        except BadRequest:
            await state.update_data(data={
                'photo_url': None
            })
            await message.answer('<b>Ссылка на фото недействительна!!!</b>')
            keyboard = await create_post_creation_keyboard(added_name=bool(state_data.get('name')),
                                                           added_photo=False,
                                                           added_price=bool(state_data.get('price')),
                                                           added_description=bool(state_data.get('description')))
            await message.answer(text='\n\n'.join(add_to_post),
                                 reply_markup=keyboard)
    else:
        keyboard = await create_post_creation_keyboard(added_name=bool(state_data.get('name')),
                                                       added_photo=False,
                                                       added_price=bool(state_data.get('price')),
                                                       added_description=bool(state_data.get('description')))
        await message.answer(text='\n\n'.join(add_to_post),
                             reply_markup=keyboard)

    await Create_post.post_creation.set()
