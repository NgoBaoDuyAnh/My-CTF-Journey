from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Post(BaseModel):
    post_id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    author: UUID
