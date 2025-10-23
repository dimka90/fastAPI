from dataclasses import dataclass, field
from app.models.post import Post
from app.models.user import UserInDb
from typing import Dict, List
@dataclass
class DataBase:
    _users: Dict[int, UserInDb] = field(default_factory=dict)
    _posts: Dict[int, List[Post]] = field(default_factory=dict)

    def add_user(self, user: UserInDb) -> UserInDb | bool:
        user_exit = self.get_user(user.id)
        if  user_exit:
            return False
        else:
            self._users[user.id] = user

        return self._users[user.id]
    
    def get_user(self, user_id:int ) -> UserInDb| None:
        return self._users.get(user_id)
    def add_post(self,user_id:int,  post: Post) ->bool:
        if user_id not in self._users:
            return False
        self._posts.setdefault(user_id, []).append(post)
        return True
    
    def get_posts(self, id: int) -> List[Post] | None:
        return self._posts[id]
    
database_instance = DataBase()
