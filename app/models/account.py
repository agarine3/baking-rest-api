from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AccountType(enum.Enum):
    """Enumeration for different types of bank accounts."""
    CHECKING = "checking"
    SAVINGS = "savings"
    MONEY_MARKET = "money_market"
    CERTIFICATE_OF_DEPOSIT = "certificate_of_deposit"
    BUSINESS = "business"


class AccountStatus(enum.Enum):
    """Enumeration for account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class Account(Base):
    """Account model representing bank accounts."""
    
    __tablename__ = "accounts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Account information
    account_number = Column(String(20), unique=True, index=True, nullable=False)
    routing_number = Column(String(9), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    
    # Balance information
    balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    available_balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Account settings
    is_overdraft_protected = Column(Boolean, default=False)
    overdraft_limit = Column(Numeric(15, 2), default=0.00)
    daily_transfer_limit = Column(Numeric(15, 2), default=10000.00)
    daily_withdrawal_limit = Column(Numeric(15, 2), default=1000.00)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", foreign_keys="Transaction.account_id", back_populates="account", cascade="all, delete-orphan")
    statements = relationship("Statement", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Account(id={self.id}, account_number='{self.account_number}', type='{self.account_type.value}', balance={self.balance})>"
