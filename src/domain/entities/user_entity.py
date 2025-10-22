from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    DELETED = "DELETED"

class UserRole(Enum):
    ADMIN = "ADMIN"
    CONTRACTOR = "CONTRACTOR"
    HAULER = "HAULER"
    SUBHAULER = "SUBHAULER"

@dataclass
class UserEntity:
    """User entity - core business object"""
    id: str
    first_name: str
    last_name: str
    email: str
    status: UserStatus
    roles: List[UserRole]
    created_at: datetime
    updated_at: datetime
    phone: Optional[str] = None
    
    def __post_init__(self):
        if not self.roles:
            raise ValueError("User must have at least one role")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
    
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE
    
    def has_role(self, role: UserRole) -> bool:
        return role in self.roles
    
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def activate(self):
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.now(datetime.timezone.utc)
    
    def deactivate(self):
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.now(datetime.timezone.utc)