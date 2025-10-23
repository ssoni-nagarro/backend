from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    """Email value object - immutable"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError(f"Invalid email: {self.value}")
    
    def _is_valid(self) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, self.value))
    
    def __str__(self) -> str:
        return self.value