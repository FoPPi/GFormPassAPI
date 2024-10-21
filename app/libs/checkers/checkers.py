from datetime import date

from app.core.config import settings
from app.db.users import delete_user

_api_key: str = settings.API_KEY
_admin_key: str = settings.ADMIN_KEY
_donatello_key: str = settings.DONATELLO_KEY


async def check_user_key_end_date(user: dict, subscription_key: str) -> bool:

    current_date = date.today()

    if current_date > user['end_date']:
        await delete_user(subscription_key)
        return False
    else:
        return True

async def check_user_key_activation(user: dict) -> bool:

    if user['active']:
        return True
    else:
        return False

async def check_user_day_limit(user: dict, subscription_key: str) -> bool:

    if user['day_limit'] > 0:
        # await use_user_day_limit(subscription_key)
        return True
    else:
        return False

async def check_api_key(api_key: str) -> bool:
    return api_key == _api_key

async def check_donatello_key(donatello_key: str) -> bool:
    return donatello_key == _donatello_key

async def check_admin_key(admin_key: str) -> bool:
    return admin_key == _admin_key