import secrets
import string
import os
from uuid import UUID
from typing import Dict, ClassVar, Optional, Union

from models.user import User
from utils import hash_md5


_admin_user_id = os.getenv("SECRET")
_admin_username = "admin_" + "".join(
    secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8)
)
_admin_password = secrets.token_urlsafe(32)


class UserRepository:
    _instance: ClassVar[Optional["UserRepository"]] = None
    _db: Dict[str, User] = {
        _admin_username: User(
            user_id=_admin_user_id,
            username=_admin_username,
            password=hash_md5(_admin_password.encode()),
            is_admin=True,
        )
    }

    @classmethod
    def _get_instance(cls) -> "UserRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def get_user_by_name(username) -> User:
        user = UserRepository._db.get(username)
        if user is None:
            raise ValueError()
        return user

    @staticmethod
    def get_user(filter: Dict) -> User:
        user_id = filter.get("user_id")
        username = filter.get("username")
        email = filter.get("email")
        is_admin = filter.get("is_admin")

        if user_id is None and username is None and email is None and is_admin is None:
            raise ValueError

        for user in UserRepository._db.values():
            if user_id is not None and str(user.user_id) != str(user_id):
                continue

            if username is not None and user.username != username:
                continue

            if email is not None and user.email != email:
                continue

            if is_admin is not None and user.is_admin != is_admin:
                continue

            return user

        raise ValueError

    @staticmethod
    def new_user(user: User) -> None:
        if user.username in UserRepository._db:
            raise ValueError()

        UserRepository._db[user.username] = user

    @staticmethod
    def subscribe_user(
        current_user_id: Union[UUID, str], target_user_id: Union[UUID, str]
    ) -> None:
        target_user = UserRepository.get_user({"user_id": target_user_id})
        target_user.subscribers.add(current_user_id)
        UserRepository._db[target_user.username] = target_user

        current_user = UserRepository.get_user({"user_id": current_user_id})
        current_user.following.add(target_user_id)
        UserRepository._db[current_user.username] = current_user

    @staticmethod
    def get_following(user_id: Union[UUID, str]) -> list:
        current_user = UserRepository.get_user({"user_id": user_id})
        result = []
        for fid in current_user.following:
            try:
                u = UserRepository.get_user({"user_id": fid})
                result.append({"user_id": str(u.user_id), "username": u.username})
            except ValueError:
                pass
        return result
 