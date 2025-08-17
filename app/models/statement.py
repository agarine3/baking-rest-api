from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Statement(Base):
    """Statement model representing monthly account statements."""
    
    __tablename__ = "statements"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Statement information
    statement_number = Column(String(50), unique=True, index=True, nullable=False)
    statement_period_start = Column(DateTime(timezone=True), nullable=False)
    statement_period_end = Column(DateTime(timezone=True), nullable=False)
    
    # Account information
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Balance information
    opening_balance = Column(Numeric(15, 2), nullable=False)
    closing_balance = Column(Numeric(15, 2), nullable=False)
    total_deposits = Column(Numeric(15, 2), default=0.00)
    total_withdrawals = Column(Numeric(15, 2), default=0.00)
    total_fees = Column(Numeric(15, 2), default=0.00)
    total_interest = Column(Numeric(15, 2), default=0.00)
    
    # Transaction counts
    total_transactions = Column(Integer, default=0)
    deposits_count = Column(Integer, default=0)
    withdrawals_count = Column(Integer, default=0)
    
    # Statement details
    currency = Column(String(3), default="USD", nullable=False)
    is_generated = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    generated_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    account = relationship("Account", back_populates="statements")
    
    def __repr__(self):
        return f"<Statement(id={self.id}, statement_number='{self.statement_number}', period='{self.statement_period_start.date()} to {self.statement_period_end.date()}', closing_balance={self.closing_balance})>"
    
    @property
    def net_change(self):
        """Calculate the net change in balance for the statement period."""
        return self.closing_balance - self.opening_balance
