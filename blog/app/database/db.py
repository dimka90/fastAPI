from dataclasses import dataclass, field
from app.models.post import Post
from typing import Dict, List
@dataclass
class DataBase:
    _db: Dict[int, List[Post]] = field(default_factory=dict)

    def add(self, post: Post) ->bool:
        author_id = post.author_id
        if author_id not in self._db:
            self._db[author_id] = []
        self._db[author_id].append(post)
        return True
    
    def get(self, id: int) -> List[Post] | None:
        if not id in self._db:
            return None
        return self._db[id]