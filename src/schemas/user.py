# --------------------------------------------------------------------------
# User schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime, date
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_serializer
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr = Field(
        ..., title="User's Email", description="유저의 이메일 주소입니다."
    )
    bio: str = Field(None, title="User's bio", description="유저의 한줄 소개입니다.")
    firstName: str = Field(
        ..., title="User's first name", description="유저의 실제 이름입니다."
    )
    lastName: str = Field(
        ..., title="User's last name", description="유저의 실제 성입니다."
    )
    gender: str = Field(..., title="User's gender", description="유저의 성별입니다.")
    country: str = Field(..., title="User's country", description="유저의 국가입니다.")
    isActive: bool = Field(
        ..., title="User's active status", description="유저의 활성 상태입니다."
    )
    createdDate: datetime = Field(
        ...,
        title="User's account created date",
        description="유저 계정의 생성 날짜입니다.",
    )
    password: Optional[SecretStr] = Field(
        None, title="User's password", description="유저 계정의 비밀번호 입니다."
    )

    # listings: Optional[List] = List[ListingSchema]

    @field_serializer("password", when_used="json")
    def dump_secret(self, v):
        return v.get_secret_value()


class UserSchema(UserBase):
    id: UUID = Field(
        ..., title="User's ID (pk)", description="유저의 고유 식별자입니다."
    )
    userId: str = Field(..., title="User's ID", description="유저의 ID입니다.")
    roles: List[str] = Field(
        ..., title="User's roles", description="유저의 역할 목록입니다."
    )
    profileImageUrl: Optional[str] = Field(
        None,
        title="User's profile image URL",
        description="유저의 프로필 이미지 URL입니다.",
    )

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBase):
    firstName: str = Field(
        ..., title="User's first name", description="유저의 실제 이름 입니다."
    )
    lastName: str = Field(
        ..., title="User's last name", description="유저의 실제 성 입니다."
    )
    nickname: str = Field(
        ..., title="User's nickname", description="유저의 닉네임 입니다."
    )
    email: EmailStr = Field(
        ..., title="User's Email", description="유저의 이메일 주소입니다."
    )
    password: str = Field(
        ..., title="User's password", description="유저 계정의 비밀번호 입니다."
    )


class UserUpdate(BaseModel):
    bio: str = Field(None, title="User's bio", description="유저의 한줄 소개 입니다.")
    profileImg: str = Field(
        None, title="User's profile image", description="유저의 프로필 이미지 입니다."
    )
