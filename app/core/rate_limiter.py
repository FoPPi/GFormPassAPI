import time
from collections import defaultdict
from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Dict, List
from functools import wraps
from app.core.security import verify_user_key
from app.core.logger import logger
from app.db.users import use_user_day_limit

user_key_header = APIKeyHeader(name="X-User-Key")


class UserKeyRateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.limiter: Dict[str, List[float]] = defaultdict(list)

    async def is_rate_limited(self, user_key: str) -> bool:
        now = time.time()
        self.limiter[user_key] = [t for t in self.limiter[user_key] if now - t < self.period]

        if len(self.limiter[user_key]) >= self.calls:
            return True

        self.limiter[user_key].append(now)
        return False


class UserKeyRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            calls: int = 40,
            period: int = 60
    ):
        super().__init__(app)
        self.limiter = UserKeyRateLimiter(calls, period)

    async def dispatch(self, request: Request, call_next):
        user_key = request.headers.get("X-User-Key")

        if not user_key:
            return HTTPException(status_code=400, detail="X-User-Key header is missing")

        try:
            await verify_user_key(user_key)
        except HTTPException as e:
            return e

        is_limited = await self.limiter.is_rate_limited(user_key)

        if is_limited:
            logger.warning(f"Rate limit exceeded for user_key: {user_key}")
            return HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        return await call_next(request)


def user_key_rate_limit(calls: int = 40, period: int = 60):
    limiter = UserKeyRateLimiter(calls, period)

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise HTTPException(status_code=500, detail="Request object not found")

            user_key = request.headers.get("X-User-Key")
            if not user_key:
                raise HTTPException(status_code=400, detail="X-User-Key header is missing")

            try:
                await verify_user_key(user_key)
            except HTTPException as e:
                raise e

            is_limited = await limiter.is_rate_limited(user_key)

            if is_limited:
                logger.warning(f"Rate limit exceeded for user_key: {user_key}")
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )

            # TODO: Maybe find a better way to do this
            await use_user_day_limit(user_key)
            return await func(*args, **kwargs)

        return wrapper

    return decorator