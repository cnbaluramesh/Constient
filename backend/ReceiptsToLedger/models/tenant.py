from sqlalchemy import Column, Integer, String, ForeignKey
from ReceiptsToLedger.core.db import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)
