from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime, date

from app.database import get_db
from app.core.auth import get_current_active_user
from app.models import User, Account, Card, CardType, CardStatus, AccountStatus
from app.schemas.card import (
    CardCreateRequest,
    CardResponse,
    CardListResponse,
    CardStatusUpdateRequest,
    CardStatusUpdateResponse
)

router = APIRouter(prefix="/cards", tags=["cards"])


def generate_card_number() -> str:
    """Generate a unique card number (simplified for demo)"""
    return f"4{uuid.uuid4().hex[:15]}"


def generate_cvv() -> str:
    """Generate a 3-digit CVV"""
    return f"{uuid.uuid4().int % 900 + 100}"


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def issue_card(
    card_data: CardCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Issue a new card for an account"""
    
    # Get the account and verify ownership
    account = db.query(Account).filter(
        Account.id == card_data.account_id,
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
    
    # Check if user already has too many cards for this account
    existing_cards = db.query(Card).filter(
        Card.account_id == card_data.account_id,
        Card.status.in_([CardStatus.ACTIVE, CardStatus.INACTIVE])
    ).count()
    
    if existing_cards >= 3:  # Limit to 3 cards per account
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum number of cards (3) already issued for this account"
        )
    
    # Generate card details
    card_number = generate_card_number()
    cvv = generate_cvv()
    
    # Set expiry date (3 years from now)
    expiry_date = date.today().replace(year=date.today().year + 3)
    
    # Create card
    card = Card(
        card_number=card_number,
        card_type=card_data.card_type,
        status=CardStatus.ACTIVE,
        cardholder_name=f"{current_user.first_name} {current_user.last_name}",
        expiry_month=expiry_date.month,
        expiry_year=expiry_date.year,
        cvv_hash=cvv,  # In production, this should be hashed
        is_pin_set=False,
        pin_hash=None,
        is_contactless_enabled=card_data.is_contactless_enabled,
        is_international_enabled=card_data.is_international_enabled,
        daily_limit=card_data.daily_limit,
        monthly_limit=card_data.monthly_limit,
        credit_limit=card_data.credit_limit if card_data.card_type == CardType.CREDIT else None,
        user_id=current_user.id,
        account_id=account.id
    )
    
    db.add(card)
    db.commit()
    db.refresh(card)
    
    return CardResponse(
        id=card.id,
        card_number=card.card_number,
        card_type=card.card_type,
        status=card.status,
        cardholder_name=card.cardholder_name,
        expiry_month=card.expiry_month,
        expiry_year=card.expiry_year,
        is_pin_set=card.is_pin_set,
        is_contactless_enabled=card.is_contactless_enabled,
        is_international_enabled=card.is_international_enabled,
        daily_limit=str(card.daily_limit),
        monthly_limit=str(card.monthly_limit),
        credit_limit=str(card.credit_limit) if card.credit_limit else None,
        user_id=card.user_id,
        account_id=card.account_id,
        created_at=card.created_at,
        message="Card issued successfully"
    )


@router.get("/", response_model=CardListResponse)
async def list_user_cards(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all cards for the current user"""
    
    cards = db.query(Card).filter(
        Card.user_id == current_user.id
    ).order_by(Card.created_at.desc()).offset(skip).limit(limit).all()
    
    total_count = db.query(Card).filter(
        Card.user_id == current_user.id
    ).count()
    
    return CardListResponse(
        cards=[
            CardResponse(
                id=card.id,
                card_number=card.card_number,
                card_type=card.card_type,
                status=card.status,
                cardholder_name=card.cardholder_name,
                expiry_month=card.expiry_month,
                expiry_year=card.expiry_year,
                is_pin_set=card.is_pin_set,
                is_contactless_enabled=card.is_contactless_enabled,
                is_international_enabled=card.is_international_enabled,
                daily_limit=str(card.daily_limit),
                monthly_limit=str(card.monthly_limit),
                credit_limit=str(card.credit_limit) if card.credit_limit else None,
                user_id=card.user_id,
                account_id=card.account_id,
                created_at=card.created_at
            ) for card in cards
        ],
        total_count=total_count,
        message="Cards retrieved successfully"
    )


@router.get("/account/{account_id}", response_model=CardListResponse)
async def list_account_cards(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all cards for a specific account"""
    
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
    
    cards = db.query(Card).filter(
        Card.account_id == account_id
    ).order_by(Card.created_at.desc()).all()
    
    return CardListResponse(
        cards=[
            CardResponse(
                id=card.id,
                card_number=card.card_number,
                card_type=card.card_type,
                status=card.status,
                cardholder_name=card.cardholder_name,
                expiry_month=card.expiry_month,
                expiry_year=card.expiry_year,
                is_pin_set=card.is_pin_set,
                is_contactless_enabled=card.is_contactless_enabled,
                is_international_enabled=card.is_international_enabled,
                daily_limit=str(card.daily_limit),
                monthly_limit=str(card.monthly_limit),
                credit_limit=str(card.credit_limit) if card.credit_limit else None,
                user_id=card.user_id,
                account_id=card.account_id,
                created_at=card.created_at
            ) for card in cards
        ],
        total_count=len(cards),
        message="Account cards retrieved successfully"
    )


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get card details by card ID"""
    
    card = db.query(Card).filter(
        Card.id == card_id,
        Card.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found or access denied"
        )
    
    return CardResponse(
        id=card.id,
        card_number=card.card_number,
        card_type=card.card_type,
        status=card.status,
        cardholder_name=card.cardholder_name,
        expiry_month=card.expiry_month,
        expiry_year=card.expiry_year,
        is_pin_set=card.is_pin_set,
        is_contactless_enabled=card.is_contactless_enabled,
        is_international_enabled=card.is_international_enabled,
        daily_limit=str(card.daily_limit),
        monthly_limit=str(card.monthly_limit),
        credit_limit=str(card.credit_limit) if card.credit_limit else None,
        user_id=card.user_id,
        account_id=card.account_id,
        created_at=card.created_at,
        message="Card details retrieved successfully"
    )


@router.patch("/{card_id}/status", response_model=CardStatusUpdateResponse)
async def update_card_status(
    card_id: int,
    status_data: CardStatusUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update card status (activate, suspend, deactivate)"""
    
    card = db.query(Card).filter(
        Card.id == card_id,
        Card.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found or access denied"
        )
    
    # Validate status transition
    if status_data.status == CardStatus.INACTIVE and card.status == CardStatus.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card is already inactive"
        )
    
    if status_data.status == CardStatus.ACTIVE and card.status == CardStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card is already active"
        )
    
    # Update card status
    old_status = card.status
    card.status = status_data.status
    card.updated_at = datetime.now()
    
    db.commit()
    db.refresh(card)
    
    return CardStatusUpdateResponse(
        card=CardResponse(
            id=card.id,
            card_number=card.card_number,
            card_type=card.card_type,
            status=card.status,
            cardholder_name=card.cardholder_name,
            expiry_month=card.expiry_month,
            expiry_year=card.expiry_year,
            is_pin_set=card.is_pin_set,
            is_contactless_enabled=card.is_contactless_enabled,
            is_international_enabled=card.is_international_enabled,
            daily_limit=str(card.daily_limit),
            monthly_limit=str(card.monthly_limit),
            credit_limit=str(card.credit_limit) if card.credit_limit else None,
            user_id=card.user_id,
            account_id=card.account_id,
            created_at=card.created_at
        ),
        old_status=old_status,
        new_status=card.status,
        message="Card status updated successfully"
    )
