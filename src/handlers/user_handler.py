"""User Handler GraphQL Resolver - Lambda Optimized"""
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from adapters.database.session_factory import DatabaseSessionFactory
from application.services.user_service import UserService
from application.dtos.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO
from application.mappers.user_dto_mapper import UserDTOMapper
from domain.exceptions.user_exceptions import (
    UserNotFoundException, 
    UserAlreadyExistsException, 
    InvalidUserDataException
)
from orm.repositories.user_respository_impl import UserRepositoryImpl

# Lambda optimization: Create database session outside handler to reduce cold start
_session_factory = DatabaseSessionFactory()

def get_db_session():
    """Get or create database session (Lambda optimized)"""
    return _session_factory.get_session()

def handler(event, context):
    """Lambda-optimized GraphQL handler for User operations"""
    db_session = get_db_session()
    
    try:
        # Handle GraphQL request format
        if "payload" in event and "ctx" in event["payload"]:
            ctx = event["payload"]["ctx"]
            operation = ctx.get("info", {}).get("fieldName", "createUser")
            args = ctx.get("arguments", {})
        else:
            # Fallback to direct format
            operation = event.get("fieldName", "createUser")
            args = event.get("arguments", {})
        
        # Handle GraphQL input object for mutations
        if operation in ["createUser", "updateUser"] and "input" in args:
            # Extract fields from input object
            input_data = args["input"]
            if isinstance(input_data, dict):
                # Merge input fields into args
                args.update(input_data)
                # Remove the input wrapper
                args.pop("input", None)
        
        if operation == "getUser":
            return get_user_flow(db_session, args)
        elif operation == "listUsers":
            return list_users_flow(db_session, args)
        elif operation == "createUser":
            return create_user_flow(db_session, args)
        elif operation == "updateUser":
            return update_user_flow(db_session, args)
        elif operation == "deleteUser":
            return delete_user_flow(db_session, args)
        elif operation == "getUserByEmail":
            return get_user_by_email_flow(db_session, args)
        else:
            return {
                "error": f"Unsupported operation {operation}"
            }
    except Exception as e:
        return {
            "error": f"Internal server error: {str(e)}"
        }
    # Note: Don't close database session in Lambda - keep it for reuse

def create_user_flow(db_session, args):
    """Coordinate user creation"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            # Convert GraphQL args to CreateUserDTO using mapper
            create_dto = UserDTOMapper.from_graphql_args(args)
            
            # Create user
            user = user_service.create_user(create_dto)
            
            # Convert UserDTO to GraphQL response format using mapper
            response = UserDTOMapper.to_graphql_response(user)
            
            return response
        
        except UserAlreadyExistsException as e:
            return {"error": str(e)}
        except InvalidUserDataException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to create user: {str(e)}"}
    
    return {"error": "No database session available"}

def get_user_flow(db_session, args):
    """Get a single user by ID"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {"error": "User ID is required"}
            
            user = user_service.get_user_by_id(user_id)
            
            # Convert UserDTO to GraphQL response format using mapper
            return UserDTOMapper.to_graphql_response(user)
        
        except UserNotFoundException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to get user: {str(e)}"}

def get_user_by_email_flow(db_session, args):
    """Get a single user by email"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            email = args.get("email")
            if not email:
                return {"error": "Email is required"}
            
            user = user_service.get_user_by_email(email)
            
            # Convert UserDTO to GraphQL response format using mapper
            return UserDTOMapper.to_graphql_response(user)
        
        except UserNotFoundException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to get user by email: {str(e)}"}

def list_users_flow(db_session, args):
    """List users with filtering and pagination"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            # Extract pagination parameters
            skip = args.get("skip", 0)
            limit = args.get("limit", 20)
            
            # Get users from service
            users = user_service.get_all_users(skip=skip, limit=limit)
            
            return {
                "items": [UserDTOMapper.to_graphql_response(user) for user in users],
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "hasMore": len(users) == limit
                }
            }
        
        except Exception as e:
            return {"error": f"Failed to list users: {str(e)}"}

def update_user_flow(db_session, args):
    """Update an existing user"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {"error": "User ID is required"}
            
            # Convert GraphQL update args to UpdateUserDTO using mapper
            update_data = UserDTOMapper.from_graphql_update_args(args)
            
            user = user_service.update_user(user_id, update_data)
            
            # Convert UserDTO to GraphQL response format using mapper
            return UserDTOMapper.to_graphql_response(user)
        
        except UserNotFoundException as e:
            return {"error": str(e)}
        except InvalidUserDataException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to update user: {str(e)}"}

def delete_user_flow(db_session, args):
    """Delete a user by ID"""
    for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {"error": "User ID is required"}
            
            success = user_service.delete_user(user_id)
            
            if not success:
                return {"error": f"User with id {user_id} not found"}
            
            return {
                "status": "success",
                "message": f"User {user_id} deleted successfully"
            }
        
        except UserNotFoundException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to delete user: {str(e)}"}
