from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CardType(enum.Enum):
    """Enumeration for different types of cards."""
    DEBIT = "debit"
    CREDIT = "credit"
    PREPAID = "prepaid"


class CardStatus(enum.Enum):
    """Enumeration for card status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    EXPIRED = "expired"
    LOST = "lost"
    STOLEN = "stolen"


class Card(Base):
    """Card model representing debit and credit cards."""
    
    __tablename__ = "cards"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Card information
    card_number = Column(String(16), unique=True, index=True, nullable=False)
    card_type = Column(Enum(CardType), nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.ACTIVE)
    
    # Cardholder information
    cardholder_name = Column(String(100), nullable=False)
    expiry_month = Column(Integer, nullable=False)
    expiry_year = Column(Integer, nullable=False)
    cvv_hash = Column(String(255), nullable=False)  # Hashed CVV for security
    
    # Security features
    is_pin_set = Column(Boolean, default=False)
    pin_hash = Column(String(255), nullable=True)  # Hashed PIN
    is_contactless_enabled = Column(Boolean, default=True)
    is_international_enabled = Column(Boolean, default=True)
    
    # Limits and settings
    daily_limit = Column(Numeric(15, 2), default=1000.00)
    monthly_limit = Column(Numeric(15, 2), default=10000.00)
    credit_limit = Column(Numeric(15, 2), nullable=True)  # For credit cards
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # For debit cards
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="cards")
    account = relationship("Account")
    
    def __repr__(self):
        return f"<Card(id={self.id}, card_number='{self.card_number[:4]}****', type='{self.card_type.value}', status='{self.status.value}')>"
    
    @property
    def is_expired(self):
        """Check if the card is expired."""
        from datetime import datetime
        current_date = datetime.now()
        return (current_date.year > self.expiry_year or 
                (current_date.year == self.expiry_year and current_date.month > self.expiry_month))
