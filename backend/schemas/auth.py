"""
Pydantic Schemas for Authentication
Request/response models for user auth endpoints
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ============================================================================
# User Registration
# ============================================================================

class UserRegister(BaseModel):
    """Request schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "trader_john",
                "email": "john@example.com",
                "password": "SecurePass123!"
            }
        }
    )


# ============================================================================
# User Login
# ============================================================================

class UserLogin(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!"
            }
        }
    )


# ============================================================================
# Token Response
# ============================================================================

class Token(BaseModel):
    """Response schema for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    """Request schema for token refresh"""
    refresh_token: str


# ============================================================================
# User Response (Public Data)
# ============================================================================

class UserResponse(BaseModel):
    """Response schema for user data (excludes password)"""
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserWithToken(BaseModel):
    """Response schema for login/register (user + token)"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ============================================================================
# Password Change
# ============================================================================

class PasswordChange(BaseModel):
    """Request schema for password change"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


# ============================================================================
# User Update
# ============================================================================

class UserUpdate(BaseModel):
    """Request schema for updating user profile"""
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "new_username",
                "email": "newemail@example.com"
            }
        }
    )
