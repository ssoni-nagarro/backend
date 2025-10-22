from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.entities.user_entity import UserEntity
from domain.repositories.user_repository import UserRepository
from orm.models.user_model import UserModel
from orm.mappers.user_model_mapper import UserModelMapper


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def create(self, user: UserEntity) -> UserEntity:
        model = UserModelMapper.to_model(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return UserModelMapper.to_entity(model)

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
