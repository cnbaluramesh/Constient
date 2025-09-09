from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ReceiptsToLedger.core.db import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    invoice_no = Column(String, unique=True, nullable=False)
    amount_due = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)

    # 👇 add reverse relationship
    matches = relationship("Match", back_populates="invoice")
