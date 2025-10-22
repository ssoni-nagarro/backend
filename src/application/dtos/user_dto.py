from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserDTO:
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class UpdateUserDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None