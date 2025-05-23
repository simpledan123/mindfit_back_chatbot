from typing import Optional
from enum import Enum

from pydantic import BaseModel, model_validator, field_validator, EmailStr

from models.user import UserRole

class UserRead(BaseModel):
    id: int
    nickname: str
    role: UserRole

class UserCreate(BaseModel):
    email: EmailStr
    nickname: str
    password1: str
    password2: str

    @model_validator(mode="before")
    def validate_not_empty(cls, values: dict) -> dict:
        for field, value in values.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"'{field}' 필드는 빈 문자열이 될 수 없습니다.")
        return values

    @model_validator(mode="after")
    def validate_password_match(self):
        if self.password1 != self.password2:
            raise ValueError("패스워드가 맞지 않습니다.")
        return self

class UserUpdate(BaseModel):
    nickname: Optional[str] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password1: str
    new_password2: str

    @model_validator(mode="after")
    def validate_new_password_match(self):
        if self.new_password1 != self.new_password2:
            raise ValueError("패스워드가 맞지 않습니다.")
        return self
