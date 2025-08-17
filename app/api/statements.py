from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from decimal import Decimal

from app.database import get_db
from app.core.auth import get_current_active_user
from app.models import User, Account, Transaction, Statement, TransactionType, AccountStatus
from app.schemas.statement import (
    StatementRequest,
    StatementResponse,
    StatementDetailResponse,
    StatementListResponse
)

router = APIRouter(prefix="/statements", tags=["statements"])


@router.post("/generate", response_model=StatementResponse, status_code=status.HTTP_201_CREATED)
async def generate_statement(
    statement_data: StatementRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a statement for an account between specified dates"""
    
    # Verify account ownership
    account = db.query(Account).filter(
        Account.id == statement_data.account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found or access denied"
        )
    
    if account.status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is not active"
        )
    
    # Validate date range
    start_date = statement_data.start_date
    end_date = statement_data.end_date
    
    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    # Check if date range is not too long (max 12 months)
    if (end_date - start_date).days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date range cannot exceed 12 months"
        )
    
    # Get transactions for the period
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account.id,
        Transaction.created_at >= start_date,
        Transaction.created_at <= end_date
    ).order_by(Transaction.created_at).all()
    
    # Calculate statement totals
    total_deposits = Decimal("0.00")
    total_withdrawals = Decimal("0.00")
    total_transfers_out = Decimal("0.00")
    total_transfers_in = Decimal("0.00")
    total_fees = Decimal("0.00")
    
    for transaction in transactions:
        amount = Decimal(str(transaction.amount))
        fee = Decimal(str(transaction.fee))
        
        if transaction.transaction_type == TransactionType.deposit:
            total_deposits += amount
        elif transaction.transaction_type == TransactionType.withdrawal:
            total_withdrawals += amount
        elif transaction.transaction_type == TransactionType.transfer:
            if transaction.from_account_id == account.id:
                total_transfers_out += amount
            else:
                total_transfers_in += amount
        
        total_fees += fee
    
    # Calculate net change
    net_change = total_deposits + total_transfers_in - total_withdrawals - total_transfers_out - total_fees
    
    # Generate statement number
    statement_number = f"STMT{account.account_number}{start_date.strftime('%Y%m')}{datetime.now().strftime('%H%M%S')}"
    
    # Create statement record
    statement = Statement(
        statement_number=statement_number,
        statement_period_start=start_date,
        statement_period_end=end_date,
        account_id=account.id,
        opening_balance=Decimal("0.00"),  # Would need to calculate from previous statements
        closing_balance=account.balance,
        total_deposits=total_deposits,
        total_withdrawals=total_withdrawals,
        total_fees=total_fees,
        total_interest=Decimal("0.00"),  # Would calculate based on interest rates
        total_transactions=len(transactions),
        currency=account.currency,
        is_generated=True
    )
    
    db.add(statement)
    db.commit()
    db.refresh(statement)
    
    return StatementResponse(
        id=statement.id,
        statement_number=statement.statement_number,
        statement_period_start=statement.statement_period_start.date(),
        statement_period_end=statement.statement_period_end.date(),
        account_id=statement.account_id,
        opening_balance=str(statement.opening_balance),
        closing_balance=str(statement.closing_balance),
        total_deposits=str(statement.total_deposits),
        total_withdrawals=str(statement.total_withdrawals),
        total_transfers_in="0.00",  # Not stored in model
        total_transfers_out="0.00",  # Not stored in model
        total_fees=str(statement.total_fees),
        total_interest=str(statement.total_interest),
        transaction_count=statement.total_transactions,
        currency=statement.currency,
        is_generated=statement.is_generated,
        created_at=statement.created_at,
        message="Statement generated successfully"
    )


@router.get("/account/{account_id}", response_model=StatementListResponse)
async def list_account_statements(
    account_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all statements for a specific account"""
    
    # Verify account ownership
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found or access denied"
        )
    
    # Get statements
    statements = db.query(Statement).filter(
        Statement.account_id == account_id
    ).order_by(Statement.statement_period_start.desc()).offset(skip).limit(limit).all()
    
    total_count = db.query(Statement).filter(
        Statement.account_id == account_id
    ).count()
    
    return StatementListResponse(
        statements=[
            StatementResponse(
                id=stmt.id,
                statement_number=stmt.statement_number,
                statement_period_start=stmt.statement_period_start.date(),
                statement_period_end=stmt.statement_period_end.date(),
                account_id=stmt.account_id,
                opening_balance=str(stmt.opening_balance),
                closing_balance=str(stmt.closing_balance),
                total_deposits=str(stmt.total_deposits),
                total_withdrawals=str(stmt.total_withdrawals),
                total_transfers_in="0.00",  # Not stored in model
                total_transfers_out="0.00",  # Not stored in model
                total_fees=str(stmt.total_fees),
                total_interest=str(stmt.total_interest),
                transaction_count=stmt.total_transactions,
                currency=stmt.currency,
                is_generated=stmt.is_generated,
                created_at=stmt.created_at
            ) for stmt in statements
        ],
        total_count=total_count,
        message="Statements retrieved successfully"
    )


@router.get("/{statement_id}", response_model=StatementDetailResponse)
async def get_statement_detail(
    statement_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed statement with transactions"""
    
    statement = db.query(Statement).filter(
        Statement.id == statement_id
    ).first()
    
    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statement not found"
        )
    
    # Verify account ownership
    account = db.query(Account).filter(
        Account.id == statement.account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this statement"
        )
    
    # Get transactions for this statement period
    transactions = db.query(Transaction).filter(
        Transaction.account_id == statement.account_id,
        Transaction.created_at >= statement.statement_period_start,
        Transaction.created_at <= statement.statement_period_end
    ).order_by(Transaction.created_at).all()
    
    return StatementDetailResponse(
        statement=StatementResponse(
            id=statement.id,
            statement_number=statement.statement_number,
            statement_period_start=statement.statement_period_start.date(),
            statement_period_end=statement.statement_period_end.date(),
            account_id=statement.account_id,
            opening_balance=str(statement.opening_balance),
            closing_balance=str(statement.closing_balance),
            total_deposits=str(statement.total_deposits),
            total_withdrawals=str(statement.total_withdrawals),
            total_transfers_in="0.00",  # Not stored in model
            total_transfers_out="0.00",  # Not stored in model
            total_fees=str(statement.total_fees),
            total_interest=str(statement.total_interest),
            transaction_count=statement.total_transactions,
            currency=statement.currency,
            is_generated=statement.is_generated,
            created_at=statement.created_at
        ),
        transactions=[
            {
                "id": t.id,
                "transaction_id": t.transaction_id,
                "transaction_type": t.transaction_type.value,
                "status": t.status.value,
                "amount": str(t.amount),
                "currency": t.currency,
                "fee": str(t.fee),
                "description": t.description,
                "reference": t.reference,
                "created_at": t.created_at
            } for t in transactions
        ],
        message="Statement details retrieved successfully"
    )
