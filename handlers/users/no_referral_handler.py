from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import no_ref_callback
from loader import dp


@dp.callback_query_handler(no_ref_callback.filter(action="enter_invitation_code"))
async def ask_for_invitation_code(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📲Отправьте мне свой код приглашения \n"
                              "<code>(id пользователя который вас пригласил</code>")
    await state.set_state("check_invitation_code")

