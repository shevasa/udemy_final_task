import logging
import re
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg import UniqueViolationError, DataError

from data.config import channels
from filters import Check_user_id, Check_subscription, Check_old_user
from keyboards.inline import no_refferal_keyboard, no_ref_callback, get_start_keyboard, post_callbackdata, \
    admin_panel_callback, referral_system_callback
from loader import dp, db, bot
from states import Create_post


@dp.callback_query_handler(referral_system_callback.filter(action='exit_to_start'))
@dp.callback_query_handler(admin_panel_callback.filter(action='exit_to_start'))
@dp.callback_query_handler(post_callbackdata.filter(action='post', object='post'), state=Create_post.post_creation)
@dp.message_handler(Check_old_user(), CommandStart())
@dp.callback_query_handler(no_ref_callback.filter(action="check_subscription"), Check_subscription())
@dp.message_handler(Check_user_id(), state="check_invitation_code")
@dp.message_handler(CommandStart(re.compile(r'^\d{6,12}?')))
async def bot_start_with_referral(update: Union[types.Message, types.CallbackQuery], state: FSMContext):
    if await state.get_state():
        state_data = await state.get_data()
        try:
            await db.add_product(**state_data)
            await update.message.edit_reply_markup()
            await update.message.answer("<b>Товар успешно добавлен!</b>")
        except TypeError:
            await update.message.edit_reply_markup()
            await update.message.answer(
                "<b>Для успешного создания обьявления нужно ввести все параметры!\nПопробуйте еще раз</b>")
        await state.finish()

    bot_username = (await bot.me).username
    user_id = update.from_user.id
    text = f"👋Привет, {update.from_user.full_name}!\n Твоя ссылка для приглашения друзей: https://t.me/{bot_username}?start={user_id}\n\n"

    if type(update) is types.CallbackQuery:
        message = update.message
        referral = channels[0]
    else:
        message = update
        if await state.get_state() == "check_invitation_code":
            referral = int(message.text)
            await state.reset_state()
        elif message.get_args():
            referral = int(message.get_args())
        else:
            referral = 0
    try:
        await db.add_user(user_id=user_id,
                          username=message.from_user.username,
                          full_name=message.from_user.full_name,
                          referral=referral)
        await db.add_money_by_user_id(referral)  # Добавляем деньгу если пользователь новый перешел по ссылке
    except UniqueViolationError or DataError:
        pass
    bonus = dict(await db.get_user_by_user_id(user_id)).get('money')
    text += f"Твой бонусный счёт: {bonus}UAH"
    try:
        username = dict(await db.get_user_by_user_id(referral)).get('username')
        text += f"Ты перешёл по ссылке от пользователя @{username}"
    except TypeError:
        pass
    await message.answer(text, reply_markup=await get_start_keyboard(user_id))


@dp.message_handler(state="check_invitation_code")
@dp.message_handler(CommandStart())
async def bot_start_no_referral(message: types.Message, state: FSMContext):
    answer_text = "Вы пришли не по приглашению.\n" \
                  "Для пользования ботом " \
                  "введите код приглашения или перейдите по реферальной ссылке.\n" \
                  "Или подпишитесь на канал и проверьте статус своей подписки\n\n"
    if await state.get_state():
        await state.reset_state()
    for channel_id in channels:
        channel = await bot.get_chat(chat_id=channel_id)
        invite_link = await channel.export_invite_link()
        answer_text += f"Канал: <a href='{invite_link}'>{channel.title}</a>"
    await message.answer(answer_text, reply_markup=no_refferal_keyboard)

# @dp.message_handler(content_types=types.ContentType.PHOTO)
# async def photo(message: types.Message):
#     await message.answer(f"{message.photo[-1].file_id}")
