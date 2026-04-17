import security
import jwt

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import User, Post, Comment, Like
from database import get_db
from schemas import UserCreate, UserOut, PostCreate, PostOut, Token, CommentCreate, CommentOut, LikeOut



users_router = APIRouter(prefix='/api/users', tags=["Users"])
posts_router = APIRouter(prefix='/api/posts', tags=["Posts"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati tugagan",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise credentials_exception
    return user


@users_router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(select(User).where(User.username == user_in.username))
    if existing_user:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi nomi band")

    user_dict = user_in.model_dump()
    hashed_password = security.get_password_hash(user_dict.pop("password"))
    
    new_user = User(**user_dict, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@users_router.post('/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == form.username))
    if not user:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usename yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User).options(selectinload(User.posts))).all()
    return users


@users_router.get('/me', response_model=UserOut)
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return current_user


@posts_router.post("/", response_model=PostOut)
def create_post(post_in: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = Post(**post_in.model_dump(), user_id=current_user.id)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@posts_router.post("/comments", response_model=CommentOut)
def create_comment(comment_in: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_comment = Comment(**comment_in.model_dump(), user_id=current_user.id)
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@posts_router.post("/{post_id}/like")
def toggle_like(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = db.scalar(select(Like).where(Like.post_id == post_id, Like.user_id == current_user.id))
    
    if like:
        db.delete(like)
        db.commit()
        return {"message": "Like olib tashlandi"}
    
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    return {"message": "Like bosildi"}


@posts_router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), search: Optional[str] = ""):
    query = select(Post).options(selectinload(Post.likes), selectinload(Post.comments))
    if search:
        query = query.where(Post.title.contains(search))

    posts = db.scalars(query).all()
    return posts


@posts_router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post_in: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.scalar(select(Post).where(Post.id == post_id, Post.user_id == current_user.id))
    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    for key, value in post_in.model_dump().items():
        setattr(post, key, value)
        
    db.commit()
    db.refresh(post)

    return post



@posts_router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.scalar(select(Post).where(Post.id == post_id, Post.user_id == current_user.id))
    if not post:
        raise HTTPException(status_code=404, detail="Bunday post mavjud emas.")
    
    db.delete(post)
    db.commit()

    return {"message": "Post o'chirildi!"}