from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from schemas import PostCreate, PostOut, UserCreate, UserOut
from database import Base, get_db, engine
from models import Post, User



Base.metadata.create_all(bind=engine)
users_router = APIRouter(prefix='/api/users', tags=["Users"])
posts_router = APIRouter(prefix='/api/posts', tags=["Posts"])



@users_router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@users_router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).options(selectinload(User.posts)).all()
    return users



@users_router.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(selectinload(User.posts)).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")

    return user


@users_router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Bunday user mavjud emas.")
    
    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    db.commit()
    db.refresh(user)

    return user


@users_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Bunday user mavjud emas.")
    
    db.delete(user)
    db.commit()

    return {"message": "User o'chirildi!"}


@posts_router.post("/", response_model=PostOut)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    user = db.get(User, post_in.user_id)
    if not user:
        raise HTTPException(status_code=400, detail=f"{post_in.user_id} idli user mavjud emas")
    
    post = Post(**post_in.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@posts_router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    stmt = select(Post)
    posts = db.scalars(stmt).all()
    return posts


@posts_router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post_in: PostCreate, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    post.title = post_in.title
    post.content = post_in.content
    db.commit()
    db.refresh(post)

    return post



@posts_router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    db.delete(post)
    db.commit()

    return {"message": "Post o'chirildi!"}
