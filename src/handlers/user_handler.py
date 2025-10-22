"""User Handler GraphQL Resolver"""
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from adapters.database.db_session import DatabaseSession
from application.services.user_service import UserService
from application.dtos.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO
from domain.exceptions.user_exceptions import (
    UserNotFoundException, 
    UserAlreadyExistsException, 
    InvalidUserDataException
)
from orm.repositories.user_respository_impl import UserRepositoryImpl

def get_user_service():
    """Get user service with database session"""
    db_session = DatabaseSession("sqlite+aiosqlite:///./test.db")
    # Note: In a real implementation, you'd want to manage the session lifecycle properly
    # This is a simplified version for the GraphQL handler pattern
    return db_session

def handler(event, context):
    """Domain-level GraphQL handler for User operations"""
    db_session = get_user_service()
    
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
    finally:
        # Close database session
        if hasattr(db_session, 'close'):
            db_session.close()

async def create_user_flow(db_session, args):
    """Coordinate user creation"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            # Create user DTO from arguments
            create_dto = CreateUserDTO(
                email=args.get("email"),
                first_name=args.get("firstName"),
                last_name=args.get("lastName"),
                phone=args.get("phone"),
                roles=args.get("roles", ["CONTRACTOR"])
            )
            
            # Create user
            user = await user_service.create_user(create_dto)
            
            return {
                "status": "success",
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "phone": user.phone,
                "status": user.status.value,
                "roles": [role.value for role in user.roles],
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
        
        except UserAlreadyExistsException as e:
            return {
                "error": str(e)
            }
        except InvalidUserDataException as e:
            return {
                "error": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to create user: {str(e)}"
            }

async def get_user_flow(db_session, args):
    """Get a single user by ID"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {
                    "error": "User ID is required"
                }
            
            user = await user_service.get_user_by_id(user_id)
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "phone": user.phone,
                "status": user.status.value,
                "roles": [role.value for role in user.roles],
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
        
        except UserNotFoundException as e:
            return {
                "error": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to get user: {str(e)}"
            }

async def get_user_by_email_flow(db_session, args):
    """Get a single user by email"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            email = args.get("email")
            if not email:
                return {
                    "error": "Email is required"
                }
            
            user = await user_service.get_user_by_email(email)
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "phone": user.phone,
                "status": user.status.value,
                "roles": [role.value for role in user.roles],
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
        
        except UserNotFoundException as e:
            return {
                "error": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to get user by email: {str(e)}"
            }

async def list_users_flow(db_session, args):
    """List users with filtering and pagination"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            filter_input = args.get("filter", {})
            
            # Extract pagination
            pagination = filter_input.get("pagination", {})
            limit = pagination.get("limit", 20)
            skip = pagination.get("skip", 0)
            
            # Extract filters
            status = filter_input.get("status")
            roles = filter_input.get("roles")
            email_contains = filter_input.get("emailContains")
            name_contains = filter_input.get("nameContains")
            
            # Get users from service
            users = await user_service.get_all_users(skip=skip, limit=limit)
            
            # Apply additional filtering if needed
            filtered_users = users
            if status:
                filtered_users = [user for user in filtered_users if user.status.value == status]
            if roles:
                filtered_users = [user for user in filtered_users if any(role.value in roles for role in user.roles)]
            if email_contains:
                filtered_users = [user for user in filtered_users if email_contains.lower() in user.email.lower()]
            if name_contains:
                filtered_users = [user for user in filtered_users if name_contains.lower() in f"{user.first_name} {user.last_name}".lower()]
            
            return {
                "items": [
                    {
                        "id": user.id,
                        "email": user.email,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "phone": user.phone,
                        "status": user.status.value,
                        "roles": [role.value for role in user.roles],
                        "createdAt": user.created_at.isoformat(),
                        "updatedAt": user.updated_at.isoformat()
                    }
                    for user in filtered_users
                ],
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "hasMore": len(filtered_users) == limit
                }
            }
        
        except Exception as e:
            return {
                "error": f"Failed to list users: {str(e)}"
            }

async def update_user_flow(db_session, args):
    """Update an existing user"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {
                    "error": "User ID is required"
                }
            
            # Extract update fields
            update_data = UpdateUserDTO()
            if "firstName" in args:
                update_data.first_name = args["firstName"]
            if "lastName" in args:
                update_data.last_name = args["lastName"]
            if "phone" in args:
                update_data.phone = args["phone"]
            if "status" in args:
                from domain.entities.user_entity import UserStatus
                update_data.status = UserStatus(args["status"])
            
            user = await user_service.update_user(user_id, update_data)
            
            return {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "phone": user.phone,
                "status": user.status.value,
                "roles": [role.value for role in user.roles],
                "createdAt": user.created_at.isoformat(),
                "updatedAt": user.updated_at.isoformat()
            }
        
        except UserNotFoundException as e:
            return {
                "error": str(e)
            }
        except InvalidUserDataException as e:
            return {
                "error": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to update user: {str(e)}"
            }

async def delete_user_flow(db_session, args):
    """Delete a user by ID"""
    async for session in db_session.get_session():
        user_repository = UserRepositoryImpl(session)
        user_service = UserService(user_repository)
        
        try:
            user_id = args.get("id")
            if not user_id:
                return {
                    "error": "User ID is required"
                }
            
            success = await user_service.delete_user(user_id)
            
            if not success:
                return {
                    "error": f"User with id {user_id} not found"
                }
            
            return {
                "status": "success",
                "message": f"User {user_id} deleted successfully"
            }
        
        except UserNotFoundException as e:
            return {
                "error": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to delete user: {str(e)}"
            }
