from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models import TransactionType, TransactionStatus


class TransactionCreateRequest(BaseModel):
    """Schema for transaction creation request."""
    account_id: int = Field(..., description="Account ID")
    transaction_type: TransactionType = Field(..., description="Type of transaction")
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    description: Optional[str] = Field(None, max_length=255, description="Transaction description")
    reference: Optional[str] = Field(None, max_length=50, description="Reference number")


class TransferRequest(BaseModel):
    """Schema for money transfer request."""
    from_account_id: int = Field(..., description="Source account ID")
    to_account_id: int = Field(..., description="Destination account ID")
    amount: Decimal = Field(..., gt=0, description="Transfer amount")
    description: Optional[str] = Field(None, max_length=255, description="Transfer description")
    reference: Optional[str] = Field(None, max_length=50, description="Reference number")


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    transaction_id: str
    transaction_type: TransactionType
    status: TransactionStatus
    amount: str
    currency: str
    fee: str
    account_id: int
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    created_at: datetime
    message: Optional[str] = None

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """Schema for transaction list response."""
    transactions: list[TransactionResponse]
    total_count: int
    message: str = Field(default="Transactions retrieved successfully")


class TransferResponse(BaseModel):
    """Schema for transfer response."""
    from_transaction: TransactionResponse
    to_transaction: TransactionResponse
    message: str = Field(default="Transfer completed successfully")
