import base64

from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.user.dependencies import authenticate_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            try:
                scheme, credentials = auth.split()
                if scheme.lower() == 'basic':
                    decoded = base64.b64decode(credentials).decode("ascii")
                    username, _, password = decoded.partition(":")
                    request.state.user = await authenticate_user(username, password)
            except (ValueError, UnicodeDecodeError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid basic auth credentials"
                )

        response = await call_next(request)
        return response
