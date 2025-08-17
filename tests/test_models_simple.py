import pytest
from sqlalchemy import text
from app.database import get_db
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


def test_model_attributes():
    """Test that models have expected attributes without instantiating them."""
    # Test User model attributes
    assert hasattr(User, '__tablename__')
    assert User.__tablename__ == 'users'
    
    # Test Account model attributes
    assert hasattr(Account, '__tablename__')
    assert Account.__tablename__ == 'accounts'
    
    # Test Transaction model attributes
    assert hasattr(Transaction, '__tablename__')
    assert Transaction.__tablename__ == 'transactions'
    
    # Test Card model attributes
    assert hasattr(Card, '__tablename__')
    assert Card.__tablename__ == 'cards'
    
    # Test Statement model attributes
    assert hasattr(Statement, '__tablename__')
    assert Statement.__tablename__ == 'statements'


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
        
        print(f"Found tables: {tables}")
        
    finally:
        db.close()


def test_table_columns():
    """Test that tables have the expected columns."""
    db = next(get_db())
    try:
        # Test users table columns
        result = db.execute(text("PRAGMA table_info(users)"))
        user_columns = [row[1] for row in result.fetchall()]
        expected_user_columns = ['id', 'first_name', 'last_name', 'email', 'phone', 'password_hash', 'is_active', 'is_verified']
        for col in expected_user_columns:
            assert col in user_columns, f"Column {col} not found in users table"
        
        # Test accounts table columns
        result = db.execute(text("PRAGMA table_info(accounts)"))
        account_columns = [row[1] for row in result.fetchall()]
        expected_account_columns = ['id', 'account_number', 'routing_number', 'account_type', 'status', 'balance', 'available_balance', 'currency']
        for col in expected_account_columns:
            assert col in account_columns, f"Column {col} not found in accounts table"
            
    finally:
        db.close()
