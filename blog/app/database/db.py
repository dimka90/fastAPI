from dataclasses import dataclass, field
from app.models.post import Post,PostInDb, PostUpdate
from app.models.user import UserInDb
from typing import Dict, List, Optional
from datetime import datetime
@dataclass
class DataBase:
    _users: Dict[int, UserInDb] = field(default_factory=dict)
    _posts: Dict[int, List[Post]] = field(default_factory=dict)
    _id = 0
    def add_user(self, user: UserInDb) -> UserInDb | bool:
        user_exit = self.get_user(user.id)
        if  user_exit:
            return False
        else:
            self._users[user.id] = user

        return self._users[user.id]
    
    def get_user(self, user_id:int ) -> UserInDb| None:
        return self._users.get(user_id)
    def add_post(self,user_id:int,  post: PostInDb) ->bool:
        if user_id not in self._users:
            return False
        self._posts.setdefault(user_id, []).append(post)
        return True
    
    def get_posts(self, id: int) -> List[PostInDb] | None:
        return self._posts.get(id, [])
    def post_id(self)-> int:
        self._id += 1
        return self._id
    def update_post(self,posts: List[PostInDb], post_id: int, filter_post: PostUpdate) -> PostInDb | None:
        for i, post in enumerate(posts):
            if post.id == post_id:
                current_data = post.model_dump()
                current_data.update(filter_post)
                updated_post = PostInDb(**current_data)
                updated_post.updated_at=datetime.utcnow()
                posts[i]=updated_post
                return  updated_post
        return None
database_instance = DataBase()
