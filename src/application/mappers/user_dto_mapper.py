from domain.entities.user_entity import UserEntity, UserStatus, UserRole
from application.dtos.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO
from typing import Dict, Any, List

class UserDTOMapper:
    @staticmethod
    def to_dto(user: UserEntity) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email,
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
        from datetime import datetime, timezone
        import uuid
        
        return UserEntity(
            id=str(uuid.uuid4()),
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone=dto.phone,
            status=UserStatus.PENDING_VERIFICATION,
            roles=dto.roles or [UserRole.CONTRACTOR],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    
    @staticmethod
    def from_graphql_args(args: Dict[str, Any]) -> CreateUserDTO:
        """Convert GraphQL arguments to CreateUserDTO"""
        # Convert roles from string values to UserRole enums if provided
        roles = args.get("roles", ["CONTRACTOR"])
        if roles and isinstance(roles[0], str):
            roles = [UserRole(role) for role in roles]
        
        return CreateUserDTO(
            email=args.get("email"),
            first_name=args.get("firstName"),
            last_name=args.get("lastName"),
            phone=args.get("phone"),
            roles=roles
        )
    
    @staticmethod
    def from_graphql_update_args(args: Dict[str, Any]) -> UpdateUserDTO:
        """Convert GraphQL update arguments to UpdateUserDTO"""
        update_dto = UpdateUserDTO()
        
        if "firstName" in args:
            update_dto.first_name = args["firstName"]
        if "lastName" in args:
            update_dto.last_name = args["lastName"]
        if "phone" in args:
            update_dto.phone = args["phone"]
        if "status" in args:
            update_dto.status = UserStatus(args["status"])
        
        return update_dto
    
    @staticmethod
    def to_graphql_response(user_dto: UserDTO) -> Dict[str, Any]:
        """Convert UserDTO to GraphQL response format"""
        return {
            "id": user_dto.id,
            "email": user_dto.email,
            "firstName": user_dto.first_name,
            "lastName": user_dto.last_name,
            "phone": user_dto.phone,
            "status": user_dto.status.value,
            "roles": [role.value for role in user_dto.roles],
            "createdAt": user_dto.created_at,
            "updatedAt": user_dto.updated_at
        }