from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from domain.entities.user_entity import UserStatus, UserRole

@dataclass
class UserDTO:
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    status: UserStatus
    roles: List[UserRole]
    created_at: datetime
    updated_at: datetime

@dataclass
class CreateUserDTO:
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    roles: List[UserRole] = None

@dataclass
class UpdateUserDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[UserStatus] = None