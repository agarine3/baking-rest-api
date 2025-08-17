from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserSignupRequest(BaseModel):
    """Schema for user signup request."""
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    address_line1: Optional[str] = Field(None, max_length=200, description="Address line 1")
    address_line2: Optional[str] = Field(None, max_length=200, description="Address line 2")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=50, description="State")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    country: Optional[str] = Field(None, max_length=100, description="Country")


class UserLoginRequest(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)."""
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    is_active: bool
    is_verified: bool
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserSignupResponse(BaseModel):
    """Schema for user signup response."""
    user: UserResponse
    message: str = Field(default="User created successfully", description="Success message")


class LoginResponse(BaseModel):
    """Schema for login response."""
    user: UserResponse
    token: TokenResponse
    message: str = Field(default="Login successful", description="Success message")
