from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.logger import logger
from app.db.users import select_user
from app.libs.checkers import check_api_key, check_user_key_end_date, check_donatello_key, check_user_key_activation, \
    check_user_day_limit
from app.libs.checkers.checkers import check_admin_key

api_key_header = APIKeyHeader(name="X-Api-Key")
user_key_header = APIKeyHeader(name="X-User-Key")
admin_key_header = APIKeyHeader(name="X-Admin-Key")
donatello_key_header = APIKeyHeader(name="X-Key")


async def verify_api_key(api_key: str = Depends(api_key_header)):
    logger.info(f"Verifying api_key: {api_key}")
    if not await check_api_key(api_key):
        logger.error(f"Invalid api_key: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key

async def verify_user_key(user_key: str = Depends(user_key_header)):
    logger.info(f"Verifying user_key: {user_key}")

    user: dict = await select_user(user_key)

    if not await check_user_key_activation(user):
        logger.error(f"Key is not active for user_key: {user_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Key is not active"
        )

    if not await check_user_key_end_date(user, user_key):
        logger.error(f"Subscription is expired for user_key: {user_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Subscription is expired"
        )

    if not await check_user_day_limit(user, user_key):
        logger.error(f"Day limit is exceeded for user_key: {user_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Day limit is exceeded"
        )

    return user_key

async def verify_donatello_key(donatello_key: str = Depends(donatello_key_header)):
    logger.info(f"Verifying donatello_key: {donatello_key}")
    if not await check_donatello_key(donatello_key):
        logger.error(f"Invalid donatello_key: {donatello_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Donatello key"
        )
    return donatello_key

async def verify_admin_key(admin_key: str = Depends(admin_key_header)):
    logger.info(f"Verifying admin_key: {admin_key}")
    if not await check_admin_key(admin_key):
        logger.error(f"Invalid admin_key: {admin_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid key"
        )
    return admin_key