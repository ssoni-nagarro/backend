from domain.entities.user_entity import UserEntity
from domain.value_objects.email import Email
from orm.models.user_model import UserModel


class UserModelMapper:
    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=Email(model.email),
            first_name=model.first_name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone_number=entity.phone_number,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )