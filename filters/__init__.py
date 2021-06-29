from aiogram import Dispatcher

from .check_invitation_code import Check_user_id

from loader import dp
# from .is_admin import AdminFilter
from .check_old_user import Check_old_user
from .check_subscription_filter import Check_subscription

if __name__ == "filters":
    dp.filters_factory.bind(Check_user_id)
    dp.filters_factory.bind(Check_subscription)
    dp.filters_factory.bind(Check_old_user)

