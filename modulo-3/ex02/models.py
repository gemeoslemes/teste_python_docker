from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import List
import enum
import datetime

class Base(DeclarativeBase):  # ✅ Agora está corretamente definido
    pass

class OperationType(enum.Enum):
    debit = "debit"
    credit = "credit"

class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    operations: Mapped[List["Operation"]] = relationship(back_populates="account", cascade="all, delete-orphan")

class Operation(Base):
    __tablename__ = 'operations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False)
    operation: Mapped[OperationType] = mapped_column(Enum(OperationType), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    account: Mapped["Account"] = relationship(back_populates="operations")