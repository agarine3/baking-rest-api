from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


class StatementRequest(BaseModel):
    """Schema for statement request."""
    start_date: date = Field(..., description="Start date for statement period")
    end_date: date = Field(..., description="End date for statement period")
    include_transactions: bool = Field(default=True, description="Include transaction details")


class StatementResponse(BaseModel):
    """Schema for statement response."""
    id: int
    statement_number: str
    statement_period_start: datetime
    statement_period_end: datetime
    account_id: int
    opening_balance: Decimal
    closing_balance: Decimal
    total_deposits: Decimal
    total_withdrawals: Decimal
    total_fees: Decimal
    total_interest: Decimal
    total_transactions: int
    deposits_count: int
    withdrawals_count: int
    currency: str
    net_change: Decimal
    created_at: datetime
    generated_at: Optional[datetime]

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
