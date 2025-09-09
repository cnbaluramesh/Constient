from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ReceiptsToLedger.core.db import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    bank_txn_id = Column(Integer, ForeignKey("bank_transactions.id"), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    matched_by = Column(String, nullable=True)
    accepted = Column(Boolean, default=None)
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)

    # 👇 add relationships
    bank_txn = relationship("BankTransaction", back_populates="matches")
    invoice = relationship("Invoice", back_populates="matches")
