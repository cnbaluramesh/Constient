from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ReceiptsToLedger.core.db import Base

class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(Integer, primary_key=True, index=True)
    value_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    batch_id = Column(String, nullable=False, index=True)
    external_id = Column(String, unique=True, nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)

    # 👇 add reverse relationship
    matches = relationship("Match", back_populates="bank_txn")
