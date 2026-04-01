from pydantic import BaseModel, Field

class PostCreate(BaseModel):
    title: str = Field(max_length=100)
    content: str

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    content: str | None = None

class PostOut(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(max_length=100)
    content: str = Field(max_length=300)

    class Config:
        from_attributes = True
