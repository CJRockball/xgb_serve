from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    
class UserInDB(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass
