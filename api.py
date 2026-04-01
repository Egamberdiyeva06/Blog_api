from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import PostCreate, PostOut, UserCreate, UserOut
from database import Base, get_db, engine
from models import Post, User

Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/posts')


@api_router.post("/users", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(**user_in.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@api_router.post('/', response_model=PostOut)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == post_in.user_id)
    user = db.scalar(stmt)

    if user:
        raise HTTPException(status_code=400, detail=f"{post_in["user_id"]} idli user mavjud emas")
    
    post = Post(**post_in.model_dump())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@api_router.get('/', response_model=list[PostOut])
def get_posts(db = Depends(get_db)):
    stmt = select(Post)
    posts = db.scalars(stmt).all()

    return posts


@api_router.get('/{post_id}', response_model=PostOut)
def get_post(post_id: int, db = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    post = db.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="Bunday raqamli post topilmadi.")
    return post


@api_router.put('/{post_id}', response_model=PostOut)
def update_post(post_id: int, post_in: PostCreate, db=Depends(get_db)):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    post.title = post_in.title
    post.content = post_in.content

    db.commit()
    db.refresh(post)

    return post

@api_router.delete("/{post_id}")
def delete_post(post_id: int, db=Depends(get_db)):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    db.delete()
    db.commit()

    return {"massege":"Post o'chirildi!"}