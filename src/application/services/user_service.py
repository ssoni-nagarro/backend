from typing import Optional, List
from domain.repositories.user_repository import UserRepository
from application.dtos.user_dto import UserDTO, UpdateUserDTO, CreateUserDTO
from application.mappers.user_dto_mapper import UserDTOMapper
from domain.exceptions.user_exceptions import UserNotFoundException, UserAlreadyExistsException

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: CreateUserDTO) -> UserDTO:
        # Check if user already exists
        existing_user = self.user_repository.find_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {user_data.email} already exists")
        
        # Convert DTO to entity
        user_entity = UserDTOMapper.to_entity_from_create_dto(user_data)
        
        # Save user
        created_user = self.user_repository.save(user_entity)
        return UserDTOMapper.to_dto(created_user)

    def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return UserDTOMapper.to_dto(user)

    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundException(f"User with email {email} not found")
        return UserDTOMapper.to_dto(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserDTO]:
        users = self.user_repository.find_all(skip=skip, limit=limit)
        return [UserDTOMapper.to_dto(user) for user in users]

    def update_user(self, user_id: str, update_data: UpdateUserDTO) -> UserDTO:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")

        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        if update_data.phone is not None:
            user.phone = update_data.phone
        if update_data.status is not None:
            user.status = update_data.status

        updated_user = self.user_repository.update(user)
        return UserDTOMapper.to_dto(updated_user)

    def delete_user(self, user_id: str) -> bool:
        return self.user_repository.delete(user_id)
