from domain.entities.user_entity import UserEntity
from application.dtos.user_dto import UserDTO

class UserDTOMapper:
    @staticmethod
    def to_dto(user: UserEntity) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email.value,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )