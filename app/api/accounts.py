from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import secrets
import string
from app.database import get_db
from app.models import User, Account, AccountType
from app.schemas.account import (
    AccountCreateRequest,
    AccountResponse,
    AccountListResponse,
    AccountDetailResponse
)
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/accounts", tags=["accounts"])


def generate_account_number() -> str:
    """Generate a unique account number."""
    return ''.join(secrets.choice(string.digits) for _ in range(10))


def generate_routing_number() -> str:
    """Generate a routing number."""
    return ''.join(secrets.choice(string.digits) for _ in range(9))


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new bank account for the current user."""
    # Generate unique account number
    account_number = generate_account_number()
    while db.query(Account).filter(Account.account_number == account_number).first():
        account_number = generate_account_number()
    
    # Create account
    db_account = Account(
        account_number=account_number,
        routing_number=generate_routing_number(),
        account_type=account_data.account_type,
        balance=account_data.initial_deposit or 0.00,
        available_balance=account_data.initial_deposit or 0.00,
        currency=account_data.currency,
        is_overdraft_protected=account_data.is_overdraft_protected,
        overdraft_limit=account_data.overdraft_limit,
        user_id=current_user.id
    )
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return AccountResponse.from_orm(db_account)


@router.get("/", response_model=AccountListResponse)
async def list_accounts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all accounts for the current user."""
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    
    return AccountListResponse(
        accounts=[AccountResponse.from_orm(account) for account in accounts],
        total_count=len(accounts)
    )


@router.get("/{account_id}", response_model=AccountDetailResponse)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific account."""
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Get recent transactions (last 5)
    recent_transactions = db.query(Account).filter(
        Account.id == account_id
    ).first().transactions[:5] if account.transactions else []
    
    return AccountDetailResponse(
        account=AccountResponse.from_orm(account),
        user_info={
            "id": current_user.id,
            "name": f"{current_user.first_name} {current_user.last_name}",
            "email": current_user.email
        },
        recent_transactions=[{"id": t.id, "amount": t.amount, "type": t.transaction_type.value} for t in recent_transactions]
    )
