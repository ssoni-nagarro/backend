from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.entities.user_entity import UserEntity, UserStatus, UserRole
from domain.repositories.user_repository import UserRepository
from orm.models.user_model import UserModel
from orm.mappers.user_model_mapper import UserModelMapper


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: UserEntity) -> UserEntity:
        model = UserModelMapper.to_model(user)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return UserModelMapper.to_entity(model)

    def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        result = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return UserModelMapper.to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        result = self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return UserModelMapper.to_entity(model) if model else None

    def find_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        result = self.session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [UserModelMapper.to_entity(model) for model in models]

    def update(self, user: UserEntity) -> UserEntity:
        model = UserModelMapper.to_model(user)
        self.session.merge(model)
        self.session.commit()
        return user

    def delete(self, user_id: str) -> bool:
        result = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False

    def find_by_filters(self, status: Optional[UserStatus] = None, 
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
        
        result = self.session.execute(query)
        models = result.scalars().all()
        return [UserModelMapper.to_entity(model) for model in models]
