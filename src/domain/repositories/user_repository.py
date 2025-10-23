from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user_entity import UserEntity, UserStatus, UserRole

class UserRepository(ABC):
    """Repository interface - contract for persistence"""
    
    @abstractmethod
    def save(self, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        pass
    
    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def find_by_filters(self, status: Optional[UserStatus] = None, 
                        roles: Optional[List[UserRole]] = None,
                        email_contains: Optional[str] = None,
                        name_contains: Optional[str] = None,
                        skip: int = 0, limit: int = 100) -> List[UserEntity]:
        pass