from typing import Optional
from domain.repositories.user_repository import UserRepository
from application.dtos.user_dto import UserDTO, UpdateUserDTO
from application.mappers.user_dto_mapper import UserDTOMapper
from domain.exceptions.user_exceptions import UserNotFoundException

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return UserDTOMapper.to_dto(user)

    async def update_user(self, user_id: str, update_data: UpdateUserDTO) -> UserDTO:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")

        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        if update_data.phone_number is not None:
            user.phone_number = update_data.phone_number

        updated_user = await self.user_repository.update(user)
        return UserDTOMapper.to_dto(updated_user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)
