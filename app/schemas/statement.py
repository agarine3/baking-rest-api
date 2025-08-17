from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


class StatementRequest(BaseModel):
    """Schema for statement request."""
    account_id: int = Field(..., description="Account ID")
    start_date: date = Field(..., description="Start date for statement period")
    end_date: date = Field(..., description="End date for statement period")
    include_transactions: bool = Field(default=True, description="Include transaction details")


class StatementResponse(BaseModel):
    """Schema for statement response."""
    id: int
    statement_number: str
    statement_period_start: date
    statement_period_end: date
    account_id: int
    opening_balance: str
    closing_balance: str
    total_deposits: str
    total_withdrawals: str
    total_transfers_in: str
    total_transfers_out: str
    total_fees: str
    total_interest: str
    transaction_count: int
    currency: str
    is_generated: bool
    created_at: datetime
    message: Optional[str] = None

    class Config:
        from_attributes = True


class StatementDetailResponse(BaseModel):
    """Schema for detailed statement response with transactions."""
    statement: StatementResponse
    transactions: List[dict] = Field(default_factory=list, description="List of transactions")
    message: str = Field(default="Statement retrieved successfully")


class StatementListResponse(BaseModel):
    """Schema for statement list response."""
    statements: List[StatementResponse]
    total_count: int
    message: str = Field(default="Statements retrieved successfully")
