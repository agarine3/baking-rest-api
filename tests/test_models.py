import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, engine, Base
from app.models import (
    User, Account, Transaction, Card, Statement,
    AccountType, AccountStatus, TransactionType, TransactionStatus,
    CardType, CardStatus
)


def test_import_models():
    """Test that all models can be imported successfully."""
    assert User is not None
    assert Account is not None
    assert Transaction is not None
    assert Card is not None
    assert Statement is not None


def test_enum_values():
    """Test that all enum values are properly defined."""
    # Account types
    assert AccountType.CHECKING.value == "checking"
    assert AccountType.SAVINGS.value == "savings"
    assert AccountType.MONEY_MARKET.value == "money_market"
    assert AccountType.CERTIFICATE_OF_DEPOSIT.value == "certificate_of_deposit"
    assert AccountType.BUSINESS.value == "business"
    
    # Account status
    assert AccountStatus.ACTIVE.value == "active"
    assert AccountStatus.INACTIVE.value == "inactive"
    assert AccountStatus.SUSPENDED.value == "suspended"
    assert AccountStatus.CLOSED.value == "closed"
    
    # Transaction types
    assert TransactionType.DEPOSIT.value == "deposit"
    assert TransactionType.WITHDRAWAL.value == "withdrawal"
    assert TransactionType.TRANSFER.value == "transfer"
    assert TransactionType.PAYMENT.value == "payment"
    assert TransactionType.FEE.value == "fee"
    assert TransactionType.INTEREST.value == "interest"
    assert TransactionType.REFUND.value == "refund"
    
    # Transaction status
    assert TransactionStatus.PENDING.value == "pending"
    assert TransactionStatus.COMPLETED.value == "completed"
    assert TransactionStatus.FAILED.value == "failed"
    assert TransactionStatus.CANCELLED.value == "cancelled"
    assert TransactionStatus.REVERSED.value == "reversed"
    
    # Card types
    assert CardType.DEBIT.value == "debit"
    assert CardType.CREDIT.value == "credit"
    assert CardType.PREPAID.value == "prepaid"
    
    # Card status
    assert CardStatus.ACTIVE.value == "active"
    assert CardStatus.INACTIVE.value == "inactive"
    assert CardStatus.BLOCKED.value == "blocked"
    assert CardStatus.EXPIRED.value == "expired"
    assert CardStatus.LOST.value == "lost"
    assert CardStatus.STOLEN.value == "stolen"


def test_user_model_structure():
    """Test User model has expected attributes."""
    user = User()
    assert hasattr(user, 'id')
    assert hasattr(user, 'first_name')
    assert hasattr(user, 'last_name')
    assert hasattr(user, 'email')
    assert hasattr(user, 'password_hash')
    assert hasattr(user, 'is_active')
    assert hasattr(user, 'is_verified')
    assert hasattr(user, 'created_at')
    assert hasattr(user, 'updated_at')


def test_account_model_structure():
    """Test Account model has expected attributes."""
    account = Account()
    assert hasattr(account, 'id')
    assert hasattr(account, 'account_number')
    assert hasattr(account, 'account_type')
    assert hasattr(account, 'status')
    assert hasattr(account, 'balance')
    assert hasattr(account, 'available_balance')
    assert hasattr(account, 'currency')
    assert hasattr(account, 'user_id')
    assert hasattr(account, 'created_at')
    assert hasattr(account, 'updated_at')


def test_transaction_model_structure():
    """Test Transaction model has expected attributes."""
    transaction = Transaction()
    assert hasattr(transaction, 'id')
    assert hasattr(transaction, 'transaction_id')
    assert hasattr(transaction, 'transaction_type')
    assert hasattr(transaction, 'status')
    assert hasattr(transaction, 'amount')
    assert hasattr(transaction, 'currency')
    assert hasattr(transaction, 'account_id')
    assert hasattr(transaction, 'created_at')


def test_card_model_structure():
    """Test Card model has expected attributes."""
    card = Card()
    assert hasattr(card, 'id')
    assert hasattr(card, 'card_number')
    assert hasattr(card, 'card_type')
    assert hasattr(card, 'status')
    assert hasattr(card, 'cardholder_name')
    assert hasattr(card, 'expiry_month')
    assert hasattr(card, 'expiry_year')
    assert hasattr(card, 'cvv_hash')
    assert hasattr(card, 'user_id')
    assert hasattr(card, 'created_at')
    assert hasattr(card, 'updated_at')


def test_statement_model_structure():
    """Test Statement model has expected attributes."""
    statement = Statement()
    assert hasattr(statement, 'id')
    assert hasattr(statement, 'statement_number')
    assert hasattr(statement, 'statement_period_start')
    assert hasattr(statement, 'statement_period_end')
    assert hasattr(statement, 'account_id')
    assert hasattr(statement, 'opening_balance')
    assert hasattr(statement, 'closing_balance')
    assert hasattr(statement, 'currency')
    assert hasattr(statement, 'created_at')


def test_database_tables_exist():
    """Test that database tables were created successfully."""
    # Get database session
    db = next(get_db())
    try:
        # Check if tables exist by querying their names
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        
        # Check for our main tables
        assert 'users' in tables
        assert 'accounts' in tables
        assert 'transactions' in tables
        assert 'cards' in tables
        assert 'statements' in tables
        
    finally:
        db.close()
