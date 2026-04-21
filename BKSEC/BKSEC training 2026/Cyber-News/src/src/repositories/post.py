from collections import defaultdict
from typing import Dict, ClassVar, List, Optional, Union
from uuid import UUID

from models.post import Post


class PostRepository:
    _instance: ClassVar[Optional["PostRepository"]] = None
    _db: defaultdict[Union[UUID, str], Dict[UUID, Post]] = defaultdict(dict)

    @classmethod
    def _get_instance(cls) -> "PostRepository":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def get_post(user_id: Union[UUID, str], post_id: UUID) -> Post:
        post = PostRepository._db[user_id].get(post_id)
        if post is None:
            raise ValueError()
        return post

    @staticmethod
    def get_posts(user_id: Union[UUID, str]) -> List[UUID]:
        return list(PostRepository._db[user_id].keys())

    @staticmethod
    def get_all_posts(user_id: Union[UUID, str]) -> List[Post]:
        return list(PostRepository._db[user_id].values())

    @staticmethod
    def new_post(user_id: Union[UUID, str], post: Post) -> None:
        if post.post_id in PostRepository._db[user_id]:
            raise ValueError()

        PostRepository._db[user_id][post.post_id] = post
