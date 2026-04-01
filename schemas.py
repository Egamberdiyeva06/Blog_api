from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int



class PostBase(BaseModel):
    title: str = Field(max_length=100)
    content: str
    user_id: int

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id: int = Field(ge=1)

    class Config:
        from_attributes = True
