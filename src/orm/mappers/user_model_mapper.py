from domain.entities.user_entity import UserEntity, UserStatus, UserRole
from domain.value_objects.email import Email
from orm.models.user_model import UserModel


class UserModelMapper:
    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        # Convert JSON roles back to UserRole enum list
        roles = [UserRole(role) for role in model.roles] if model.roles else []
        
        return UserEntity(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            status=model.status,
            roles=roles,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        # Convert UserRole enum list to JSON-serializable list
        roles = [role.value for role in entity.roles] if entity.roles else []
        
        return UserModel(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone=entity.phone,
            status=entity.status,
            roles=roles,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )