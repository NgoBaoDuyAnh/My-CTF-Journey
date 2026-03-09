import os
import re
from uuid import UUID
from typing import Annotated, Optional, Union, Dict

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

import consts
from models.user import User
from models.token import Token, get_current_user
from repositories.user import UserRepository
from notify import send_new_subscriber_email
from utils import hash_md5

router = APIRouter()


@router.get("/users", response_model=User)
async def get_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/users/following")
async def get_following(current_user: Annotated[User, Depends(get_current_user)]) -> list:
    return UserRepository.get_following(current_user.user_id)


@router.post("/token", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    try:
        user = UserRepository.get_user_by_name(form_data.username)
        if user.password != hash_md5(form_data.password.encode()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    encoded_jwt = jwt.encode(
        user.to_dict(),
        os.getenv("JWT_SECRET_KEY"),
        algorithm=consts.JWT_ALGORITHM,
    )

    return {"access_token": encoded_jwt, "token_type": "bearer"}


class PostSignUpBody(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: PostSignUpBody) -> Union[UUID, str]:
    if body.email is not None:
        if not bool(re.match(consts.EMAIL_PATTERN, body.email)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user = User(
        username=body.username,
        password=hash_md5(body.password.encode()),
        email=body.email,
    )

    try:
        UserRepository.new_user(user)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return user.user_id


class PostSubscribeBody(BaseModel):
    target_user_id: UUID


@router.post("/subscribe")
async def subscribe(
    current_user: Annotated[User, Depends(get_current_user)], body: PostSubscribeBody
) -> None:
    if current_user.user_id == body.target_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        UserRepository.subscribe_user(current_user.user_id, body.target_user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        target_user = UserRepository.get_user({"user_id": body.target_user_id})
        if target_user.email is not None:
            await send_new_subscriber_email(target_user, current_user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
