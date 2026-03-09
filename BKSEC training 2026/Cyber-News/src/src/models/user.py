from typing import Any, Optional, Set, Dict, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: Union[UUID, str] = Field(default_factory=uuid4)
    username: str
    password: str
    email: Optional[str] = None
    is_admin: bool = False
    subscribers: Set[Union[UUID, str]] = set()
    following: Set[Union[UUID, str]] = set()

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "user_id": str(self.user_id),
            "username": self.username,
            "is_admin": self.is_admin,
        }

        if self.email is not None:
            res["email"] = self.email

        return res
