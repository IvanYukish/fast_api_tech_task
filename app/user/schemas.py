from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, validator, Field

from app.core.schemas import PyObjectId
from app.user.constants import MAX_FIRST_NAME_LEN, MAX_LAST_NAME_LEN, MIN_LAST_NAME_LEN
from app.user.enums import UserData


class UserBaseSchema(BaseModel):
    @classmethod
    def validate_name(cls, item, max_len, min_len):
        if len(item) > max_len:
            raise ValueError(f"Name length should be between {min_len} and {max_len}")
        return item

    @validator("first_name", check_fields=False)
    def validate_first_name(cls, item) -> str:
        return cls.validate_name(item, MAX_FIRST_NAME_LEN, MIN_LAST_NAME_LEN)

    @validator("last_name", check_fields=False)
    def validate_last_name(cls, item) -> str:
        return cls.validate_name(item, MAX_LAST_NAME_LEN, MIN_LAST_NAME_LEN)


class UserSchema(UserBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str
    last_name: str
    role: UserData
    is_active: bool
    created_at: Optional[str] = None
    last_login: str
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": "false",
                "created_at": "datetime",
                "last_login": "datetime",
                "password": "fakehashedsecret",
            }
        }


class UpdateUserSchema(UserBaseSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    is_active: Optional[str]
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": "false",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }


class ShowUserSchema(UpdateUserSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
