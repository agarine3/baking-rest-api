from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
import uuid
from datetime import datetime

from app.database import get_db
from app.core.auth import get_current_active_user
from app.models import User, Account, Transaction, TransactionType, TransactionStatus, AccountStatus
from app.schemas.transaction import (
    TransactionCreateRequest,
    TransferRequest,
    TransactionResponse,
    TransactionListResponse,
    TransferResponse
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


def generate_transaction_id() -> str:
    """Generate a unique transaction ID"""
    return f"TXN{uuid.uuid4().hex[:12].upper()}"


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction (deposit/withdrawal)"""
    
    # Get the account and verify ownership
    account = db.query(Account).filter(
        Account.id == transaction_data.account_id,
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
    
    # Validate transaction amount
    amount = Decimal(str(transaction_data.amount))
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction amount must be positive"
        )
    
    # For withdrawals, check sufficient balance
    if transaction_data.transaction_type == TransactionType.WITHDRAWAL:
        if account.available_balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds"
            )
        
        # Check daily withdrawal limit
        today = datetime.now().date()
        daily_withdrawals = db.query(Transaction).filter(
            Transaction.account_id == account.id,
            Transaction.transaction_type == TransactionType.WITHDRAWAL,
            Transaction.created_at >= today
        ).all()
        
        daily_total = sum(Decimal(str(t.amount)) for t in daily_withdrawals)
        if daily_total + amount > Decimal(str(account.daily_withdrawal_limit)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Daily withdrawal limit exceeded"
            )
    
    # Create transaction
    transaction = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type=transaction_data.transaction_type,
        status=TransactionStatus.PENDING,
        amount=amount,
        currency=account.currency,
        fee=Decimal("0.00"),  # No fees for basic transactions
        account_id=account.id,
        description=transaction_data.description,
        reference_number=transaction_data.reference
    )
    
    db.add(transaction)
    
    # Update account balance
    if transaction_data.transaction_type == TransactionType.DEPOSIT:
        account.balance += amount
        account.available_balance += amount
        transaction.status = TransactionStatus.COMPLETED
    else:  # withdrawal
        account.balance -= amount
        account.available_balance -= amount
        transaction.status = TransactionStatus.COMPLETED
    
    account.last_activity = datetime.now()
    db.commit()
    db.refresh(transaction)
    
    return TransactionResponse(
        id=transaction.id,
        transaction_id=transaction.transaction_id,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        amount=str(transaction.amount),
        currency=transaction.currency,
        fee=str(transaction.fee),
        account_id=transaction.account_id,
        description=transaction.description,
        reference=transaction.reference_number,
        created_at=transaction.created_at,
        message="Transaction created successfully"
    )


@router.post("/transfer", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
async def transfer_money(
    transfer_data: TransferRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Transfer money between accounts"""
    
    # Get source account and verify ownership
    from_account = db.query(Account).filter(
        Account.id == transfer_data.from_account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not from_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source account not found or access denied"
        )
    
    if from_account.status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source account is not active"
        )
    
    # Get destination account
    to_account = db.query(Account).filter(
        Account.id == transfer_data.to_account_id
    ).first()
    
    if not to_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination account not found"
        )
    
    if to_account.status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Destination account is not active"
        )
    
    # Prevent self-transfer
    if from_account.id == to_account.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to the same account"
        )
    
    # Validate transfer amount
    amount = Decimal(str(transfer_data.amount))
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfer amount must be positive"
        )
    
    # Check sufficient balance
    if from_account.available_balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    
    # Check daily transfer limit
    today = datetime.now().date()
    daily_transfers = db.query(Transaction).filter(
        Transaction.from_account_id == from_account.id,
        Transaction.transaction_type == TransactionType.TRANSFER,
        Transaction.created_at >= today
    ).all()
    
    daily_total = sum(Decimal(str(t.amount)) for t in daily_transfers)
    if daily_total + amount > Decimal(str(from_account.daily_transfer_limit)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily transfer limit exceeded"
        )
    
    # Create transfer transaction
    transfer_transaction = Transaction(
        transaction_id=generate_transaction_id(),
        transaction_type=TransactionType.TRANSFER,
        status=TransactionStatus.COMPLETED,
        amount=amount,
        currency=from_account.currency,
        fee=Decimal("0.00"),  # No fees for internal transfers
        account_id=from_account.id,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        description=transfer_data.description,
        reference_number=transfer_data.reference
    )
    
    db.add(transfer_transaction)
    
    # Update account balances
    from_account.balance -= amount
    from_account.available_balance -= amount
    from_account.last_activity = datetime.now()
    
    to_account.balance += amount
    to_account.available_balance += amount
    to_account.last_activity = datetime.now()
    
    db.commit()
    db.refresh(transfer_transaction)
    
    return TransferResponse(
        from_transaction=TransactionResponse(
            id=transfer_transaction.id,
            transaction_id=transfer_transaction.transaction_id,
            transaction_type=transfer_transaction.transaction_type,
            status=transfer_transaction.status,
            amount=str(transfer_transaction.amount),
            currency=transfer_transaction.currency,
            fee=str(transfer_transaction.fee),
            account_id=transfer_transaction.account_id,
            from_account_id=transfer_transaction.from_account_id,
            to_account_id=transfer_transaction.to_account_id,
            description=transfer_transaction.description,
            reference=transfer_transaction.reference_number,
            created_at=transfer_transaction.created_at
        ),
        to_transaction=TransactionResponse(
            id=transfer_transaction.id,
            transaction_id=transfer_transaction.transaction_id,
            transaction_type=transfer_transaction.transaction_type,
            status=transfer_transaction.status,
            amount=str(transfer_transaction.amount),
            currency=transfer_transaction.currency,
            fee=str(transfer_transaction.fee),
            account_id=to_account.id,
            from_account_id=transfer_transaction.from_account_id,
            to_account_id=transfer_transaction.to_account_id,
            description=transfer_transaction.description,
            reference=transfer_transaction.reference_number,
            created_at=transfer_transaction.created_at
        ),
        message="Transfer completed successfully"
    )


@router.get("/account/{account_id}", response_model=TransactionListResponse)
async def list_account_transactions(
    account_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List transactions for a specific account"""
    
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
    
    # Get transactions
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    
    total_count = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).count()
    
    return TransactionListResponse(
        transactions=[
            TransactionResponse(
                id=t.id,
                transaction_id=t.transaction_id,
                transaction_type=t.transaction_type,
                status=t.status,
                amount=str(t.amount),
                currency=t.currency,
                fee=str(t.fee),
                account_id=t.account_id,
                from_account_id=t.from_account_id,
                to_account_id=t.to_account_id,
                description=t.description,
                reference=t.reference_number,
                created_at=t.created_at
            ) for t in transactions
        ],
        total_count=total_count,
        message="Transactions retrieved successfully"
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get transaction details by transaction ID"""
    
    transaction = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Verify user has access to this transaction
    account = db.query(Account).filter(
        Account.id == transaction.account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this transaction"
        )
    
    return TransactionResponse(
        id=transaction.id,
        transaction_id=transaction.transaction_id,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        amount=str(transaction.amount),
        currency=transaction.currency,
        fee=str(transaction.fee),
        account_id=transaction.account_id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        description=transaction.description,
        reference=transaction.reference,
        created_at=transaction.created_at,
        message="Transaction details retrieved successfully"
    )
