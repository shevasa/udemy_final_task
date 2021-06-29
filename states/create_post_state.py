from aiogram.dispatcher.filters.state import StatesGroup, State


class Create_post(StatesGroup):
    post_creation = State()
    add_price = State()
    add_description = State()
    add_photo = State()
    add_name = State()
    submission = State()
