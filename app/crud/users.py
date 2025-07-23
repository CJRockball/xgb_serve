from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional
import uuid

class UserCRUD:
    async def get_user(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def authenticate_user(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user_crud = UserCRUD()
