import logging

from aiogram import types
from aiogram.utils import markdown

from keyboards.inline import start_keyboard_callback, referral_system_keyboard, referral_system_callback
from loader import dp, db, bot


@dp.callback_query_handler(referral_system_callback.filter(action='show_referrals'))
@dp.callback_query_handler(start_keyboard_callback.filter(move_to="referral_system"))
async def referral_system(call: types.CallbackQuery):
    bot_username = (await bot.me).username
    await call.message.edit_reply_markup()
    if call.data == 'referral_system:show_referrals':
        user_id = call.from_user.id
        referrals = [dict(referral) for referral in await db.get_user_referrals_by_user_id(user_id)]
        result = []
        for num, referral in enumerate(referrals, start=1):
            user_url = f'tg://user?id={referral.get("user_id")}'
            mention = markdown.hlink(title=str(referral.get('full_name')), url=user_url)
            text = f'<code>№{num}</code> {mention}'
            result.append(text)
        if not bool(result):
            result.append(
                f"У тебя пока что нет реферралов\nДобавляй друзей по ссылке: https://t.me/{bot_username}?start={user_id} ")
        await call.message.answer(text='<code>👇Твои реферралы👇\n\n</code>' + '\n\n'.join(result))
    await call.message.answer(text="<b>Реферральная система</b>",
                              reply_markup=referral_system_keyboard)
