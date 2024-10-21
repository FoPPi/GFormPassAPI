import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException

from app.core.logger import logger
from app.db.base import db
from app.schemas import Donate


async def generate_user_key(donate: Donate) -> str:
    if int(donate.amount) < 200 and donate.currency == 'UAH':
        logger.error("Donation amount must be greater than 200 UAH", extra=donate)
        raise HTTPException(status_code=403, detail="Donation amount must be greater than 200 UAH")
    elif int(donate.amount) < 5 and (donate.currency == 'USD' or donate.currency == 'EUR'):
        logger.error("Donation amount must be greater than 5 USD/EUR", extra=donate)
        raise HTTPException(status_code=403, detail="Donation amount must be greater than 5 USD/EUR")

    logger.info("Generate new user key", extra=donate)
    subscription_key = uuid.uuid4().__str__()
    try:
        logger.info("Insert new user key", extra=donate)
        await db.insert_data('users', {'pub_id': donate.pubId, 'subscription_key': subscription_key, 'email': donate.message})
        return subscription_key
    except Exception as e:
        logger.error("Error while generating new user key. Error: %s", e, extra=donate)
        raise HTTPException(status_code=500, detail=str(e))

async def activate_user_key(subscription_key: str) -> bool:
    logger.info("Activate user key", extra={'subscription_key': subscription_key})
    selected = await db.select_data('users', ['active'], f"subscription_key = '{subscription_key}'")

    if len(selected) == 0:
        logger.error("Key not found", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=403, detail="Key not found")
    elif selected[0]['active'] == 1:
        logger.error("Key is already active", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=403, detail="Key is already active")

    try:
        logger.info("Update user key", extra={'subscription_key': subscription_key})
        await db.update_data('users', {'active': True, 'end_date': datetime.now() + timedelta(days=30)}, f"subscription_key = '{subscription_key}'")

        return True
    except Exception as e:
        logger.error(f"Error while activating user key. Error: {e}", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=500, detail=str(e))

async def use_user_day_limit(subscription_key: str) -> bool:
    logger.info("Use user key", extra={'subscription_key': subscription_key})
    selected = await db.select_data('users', ['active', 'day_limit'], f"subscription_key = '{subscription_key}'")

    if len(selected) == 0:
        logger.error("Key not found", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=403, detail="Key not found")
    elif selected[0]['active'] == 0:
        logger.error("Key is not active", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=403, detail="Key is not active")

    try:
        logger.info("Make day limit - 1 user key", extra={'subscription_key': subscription_key, 'day_limit': selected[0]['day_limit']})
        await db.update_data('users', {'day_limit': selected[0]['day_limit'] - 1}, f"subscription_key = '{subscription_key}'")

        return True
    except Exception as e:
        logger.error(f"Error while updating day limit - 1 of user key. Error: {e}", extra={'subscription_key': subscription_key, 'day_limit': selected[0]['day_limit']})
        raise HTTPException(status_code=500, detail=str(e))

async def select_user(subscription_key: str) -> dict:
    logger.info("Select user end date", extra={'subscription_key': subscription_key})
    selected = await db.select_data('users', ['active', 'day_limit', 'end_date'], f"subscription_key = '{subscription_key}'")

    if len(selected) == 0:
        logger.error("Key not found", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=403, detail="Key not found")

    return selected[0]

async def update_users_day_limit() -> bool:
    logger.info("Update users day limit")
    try:
        await db.update_data('users', {'day_limit': 200})

        return True
    except Exception as e:
        logger.error(f"Error while updating day limit of user key. Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def delete_user(subscription_key: str) -> bool:
    try:
        logger.info("Delete user", extra={'subscription_key': subscription_key})
        await db.delete_data('users', f"subscription_key = '{subscription_key}'")

        return True
    except Exception as e:
        logger.error(f"Error while deleting user. Error: {e}", extra={'subscription_key': subscription_key})
        raise HTTPException(status_code=500, detail=str(e))
