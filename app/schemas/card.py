from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models import CardType, CardStatus


class CardCreateRequest(BaseModel):
    """Schema for card creation request."""
    card_type: CardType = Field(..., description="Type of card to create")
    cardholder_name: str = Field(..., max_length=100, description="Name on the card")
    account_id: Optional[int] = Field(None, description="Linked account ID for debit cards")
    daily_limit: Optional[Decimal] = Field(1000.00, ge=0, description="Daily spending limit")
    monthly_limit: Optional[Decimal] = Field(10000.00, ge=0, description="Monthly spending limit")
    credit_limit: Optional[Decimal] = Field(None, ge=0, description="Credit limit for credit cards")
    is_contactless_enabled: bool = Field(default=True, description="Enable contactless payments")
    is_international_enabled: bool = Field(default=True, description="Enable international transactions")


class CardResponse(BaseModel):
    """Schema for card response (without sensitive data)."""
    id: int
    card_number: str  # Will be masked in actual implementation
    card_type: CardType
    status: CardStatus
    cardholder_name: str
    expiry_month: int
    expiry_year: int
    is_contactless_enabled: bool
    is_international_enabled: bool
    daily_limit: Decimal
    monthly_limit: Decimal
    credit_limit: Optional[Decimal]
    user_id: int
    account_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    last_used: Optional[datetime]
    is_expired: bool

    class Config:
        from_attributes = True


class CardListResponse(BaseModel):
    """Schema for card list response."""
    cards: list[CardResponse]
    total_count: int
    message: str = Field(default="Cards retrieved successfully")


class CardStatusUpdateRequest(BaseModel):
    """Schema for card status update request."""
    status: CardStatus = Field(..., description="New card status")


class CardStatusUpdateResponse(BaseModel):
    """Schema for card status update response."""
    card: CardResponse
    message: str = Field(default="Card status updated successfully")
