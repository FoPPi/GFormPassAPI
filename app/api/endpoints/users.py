from fastapi import APIRouter, Depends

from app.core.security import verify_api_key, verify_donatello_key, user_key_header, verify_admin_key
from app.db.users import activate_user_key, generate_user_key, update_users_day_limit
from app.libs.mailer import Mailer
from app.schemas import Donate

router = APIRouter()

@router.post("/user/activate")
async def activate_user(
    _: str = Depends(verify_api_key),
    user_key: str = Depends(user_key_header)
):
    if await activate_user_key(user_key):
        return {"status": "success"}
    else:
        return {"status": "failed"}

@router.post("/user/donates")
async def get_donates(
    donate_data: Donate,
    _: str = Depends(verify_donatello_key)
):
    key = await generate_user_key(donate_data)
    mailer = Mailer()
    await mailer.send_mail(donate_data.message, key)
    return {"status": "success"}

@router.patch("/user/update_keys")
async def delete_user(
    _: str = Depends(verify_admin_key)
):
    await update_users_day_limit()
    return {"status": "success"}