from pydantic import BaseModel, EmailStr
from typing import Optional

# Схема для создания пользователя
class SUserCreate(BaseModel):
    username: str
    email: str
    password: str

# Схема для отображения пользователя
class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True