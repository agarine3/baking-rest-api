from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models import AccountType, AccountStatus


class AccountCreateRequest(BaseModel):
    """Schema for account creation request."""
    account_type: AccountType = Field(..., description="Type of account to create")
    initial_deposit: Optional[Decimal] = Field(0.00, ge=0, description="Initial deposit amount")
    currency: str = Field(default="USD", max_length=3, description="Account currency")
    is_overdraft_protected: bool = Field(default=False, description="Enable overdraft protection")
    overdraft_limit: Optional[Decimal] = Field(None, ge=0, description="Overdraft limit amount")


class AccountResponse(BaseModel):
    """Schema for account response."""
    id: int
    account_number: str
    routing_number: str
    account_type: AccountType
    status: AccountStatus
    balance: Decimal
    available_balance: Decimal
    currency: str
    is_overdraft_protected: bool
    overdraft_limit: Optional[Decimal]
    daily_transfer_limit: Decimal
    daily_withdrawal_limit: Decimal
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_activity: Optional[datetime]

    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    """Schema for account list response."""
    accounts: List[AccountResponse]
    total_count: int
    message: str = Field(default="Accounts retrieved successfully")


class AccountDetailResponse(BaseModel):
    """Schema for detailed account response."""
    account: AccountResponse
    user_info: dict  # Basic user info without sensitive data
    recent_transactions: List[dict] = Field(default_factory=list)
    message: str = Field(default="Account details retrieved successfully")
