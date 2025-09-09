from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from ReceiptsToLedger.core.db import Base
import enum

class Role(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.analyst, nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)
