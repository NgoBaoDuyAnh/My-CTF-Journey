from typing import Annotated, List, Union
from uuid import UUID
from urllib.parse import urlparse, unquote
import urllib.request
import os
import json

from fastapi.params import Depends
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from models.token import get_current_user
from models.user import User
from models.post import Post
from notify import send_new_post_email
from repositories.post import PostRepository

router = APIRouter()

BLOCKED_PATH_KEYWORDS = json.loads(os.getenv("BLOCKED_PATH_KEYWORDS", "[]"))


def blocked_path(url: str) -> bool:
    path = urlparse(url.strip()).path
    path_lower = path.lower()
    decoded_path_lower = unquote(path).lower()
    return any(
        keyword in path_lower or keyword in decoded_path_lower
        for keyword in BLOCKED_PATH_KEYWORDS
    )


def is_url_safe(url: str) -> bool:
    parsed = urlparse(url)
    blocked_schemes = {"file", "ftp", "gopher", "data", "javascript", "vbscript"}
    return parsed.scheme.lower() not in blocked_schemes


@router.get("/posts/{user_id}/{post_id}", response_model=Post)
async def get_post(user_id: Union[UUID, str], post_id: UUID) -> Post:
    try:
        return PostRepository.get_post(user_id, post_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/posts", response_model=List[UUID])
async def get_posts(user_id: Union[UUID, str]) -> List[UUID]:
    return PostRepository.get_posts(user_id)


@router.get("/posts/mine", response_model=List[Post])
async def get_my_posts(
    current_user: Annotated[User, Depends(get_current_user)],
) -> List[Post]:
    return PostRepository.get_all_posts(current_user.user_id)


class PostPostsBody(BaseModel):
    title: str
    content: str


@router.post("/posts")
async def new_post(
    current_user: Annotated[User, Depends(get_current_user)], body: PostPostsBody
) -> UUID:
    post = Post(
        title=body.title,
        content=body.content,
        author=current_user.user_id,
    )
    try:
        PostRepository.new_post(current_user.user_id, post)

        await send_new_post_email(current_user, post)

        return post.post_id
    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_ERROR)


class ImportPostBody(BaseModel):
    url: str


@router.post("/posts/import")
async def import_post(
    current_user: Annotated[User, Depends(get_current_user)],
    body: ImportPostBody,
) -> dict:

    if blocked_path(body.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL contains blocked path",
        )

    if not is_url_safe(body.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL scheme not allowed",
        )
    try:
        with urllib.request.urlopen(body.url) as response:
            content = response.read().decode("utf-8")

        url_path = urlparse(body.url.strip()).path
        title = os.path.basename(url_path) or "Imported Post"

        post = Post( 
            title=title,
            content=content,
            author=current_user.user_id,
        )
        PostRepository.new_post(current_user.user_id, post)

        return {
            "post_id": str(post.post_id),
            "title": post.title,
            "content": content,
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch URL",
        )
