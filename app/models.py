from pydantic import BaseModel, Field
from datetime import datetime
from typing import Set, Optional
from bson import ObjectId

# Custom Pydantic field for MongoDB ObjectId
class PyObjectId(str):
    def __new__(cls, oid = None):
        if oid is None:
            oid = ObjectId()
        elif not ObjectId.is_valid(oid):
            raise ValueError("Invalid ObjectId")
        return str.__new__(cls, str(oid))


# User model
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    roles: Set[str] = Field(default_factory=set)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

    # Additional fields can be added as needed
    class Config:
        # Config class to handle ObjectId serialization
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "
                "hashed_password": "hashedpassword123",
                "full_name": "John Doe",
                "roles": ["user", "admin"],
                "is_active": True,
                "is_superuser": False
            }
        }


# Message model
class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False
    
    
    # Additional fields can be added as needed 
    class Config:
        # Config class to handle ObjectId serialization
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "60d5f483f8d2e3b1c8e4b8a1",
                "content": "Hello, this is a message.",
                "is_read": False
            }
        }


# Room model
class Room(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    members: Set[PyObjectId] = Field(default_factory=set)
    # Additional fields can be added as needed
    class Config:
        # Config class to handle ObjectId serialization
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "General",
                "description": "A general chat room.",
                "members": ["60d5f483f8d2e3b1c8e4b8a1", "60d5f483f8d2e3b1c8e4b8a2"]
            }
        }

