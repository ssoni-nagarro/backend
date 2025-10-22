from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.entities.user_entity import UserEntity, UserStatus, UserRole
from domain.repositories.user_repository import UserRepository
from orm.models.user_model import UserModel
from orm.mappers.user_model_mapper import UserModelMapper


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserEntity) -> UserEntity:
        model = UserModelMapper.to_model(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return UserModelMapper.to_entity(model)

    async def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return UserModelMapper.to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return UserModelMapper.to_entity(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        result = await self.session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [UserModelMapper.to_entity(model) for model in models]

    async def update(self, user: UserEntity) -> UserEntity:
        model = UserModelMapper.to_model(user)
        await self.session.merge(model)
        await self.session.commit()
        return user

    async def delete(self, user_id: str) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True
        return False

    async def find_by_filters(self, status: Optional[UserStatus] = None, 
                            roles: Optional[List[UserRole]] = None,
                            email_contains: Optional[str] = None,
                            name_contains: Optional[str] = None,
                            skip: int = 0, limit: int = 100) -> List[UserEntity]:
        query = select(UserModel)
        
        if status:
            query = query.where(UserModel.status == status.value)
        if email_contains:
            query = query.where(UserModel.email.contains(email_contains))
        if name_contains:
            query = query.where(
                (UserModel.first_name.contains(name_contains)) |
                (UserModel.last_name.contains(name_contains))
            )
        
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [UserModelMapper.to_entity(model) for model in models]
