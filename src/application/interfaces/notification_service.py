from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    async def send_onboarding_complete_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def send_welcome_email(self, email: str) -> bool:
        pass