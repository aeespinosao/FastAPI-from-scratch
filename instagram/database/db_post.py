from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from models.post import Post
from datetime import datetime

def create(db: Session, request: PostBase):
    print(request.dict())
    new_post = Post(
        **request.dict(),
        timestamp=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def retrieve_all(db: Session):
    return db.query(Post).all()