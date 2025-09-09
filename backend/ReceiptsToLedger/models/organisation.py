from sqlalchemy import Column, Integer, String
from ReceiptsToLedger.core.db import Base

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
