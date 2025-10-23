class UserException(Exception):
    """Base exception for user domain"""
    pass

class UserNotFoundException(UserException):
    """User not found"""
    pass

class UserAlreadyExistsException(UserException):
    """User with email already exists"""
    pass

class InvalidUserDataException(UserException):
    """Invalid user data"""
    pass
