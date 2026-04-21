import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError

import consts
from models.user import User
from repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.getenv("JWT_SECRET_KEY"), algorithms=[consts.JWT_ALGORITHM]
        )
        user = UserRepository.get_user(payload)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except JWTError:
        raise credentials_exception
