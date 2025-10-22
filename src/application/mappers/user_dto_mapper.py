from domain.entities.user_entity import UserEntity
from application.dtos.user_dto import UserDTO, CreateUserDTO

class UserDTOMapper:
    @staticmethod
    def to_dto(user: UserEntity) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email.value,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            status=user.status,
            roles=user.roles,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    
    @staticmethod
    def to_entity_from_create_dto(dto: CreateUserDTO) -> UserEntity:
        from domain.value_objects.email import Email
        from datetime import datetime
        import uuid
        
        return UserEntity(
            id=str(uuid.uuid4()),
            email=Email(dto.email),
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone=dto.phone,
            status=UserEntity.UserStatus.PENDING_VERIFICATION,
            roles=dto.roles or [UserEntity.UserRole.CONTRACTOR],
            created_at=datetime.now(datetime.timezone.utc),
            updated_at=datetime.now(datetime.timezone.utc),
        )