from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tiffin.db")
# Fix postgres URL for SQLAlchemy (Vercel/Railway use postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    phone      = Column(String, default="")
    addr       = Column(String, default="")
    lprice     = Column(Float, default=0)
    dprice     = Column(Float, default=0)
    lunch      = Column(Boolean, default=True)
    dinner     = Column(Boolean, default=True)
    entries    = relationship("Entry", back_populates="customer", cascade="all, delete")
    payments   = relationship("Payment", back_populates="customer", cascade="all, delete")


class Entry(Base):
    __tablename__ = "entries"
    id          = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date        = Column(Date, nullable=False)
    lunch       = Column(Integer, default=0)
    dinner      = Column(Integer, default=0)
    customer    = relationship("Customer", back_populates="entries")


class Payment(Base):
    __tablename__ = "payments"
    id          = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    year        = Column(Integer, nullable=False)
    month       = Column(Integer, nullable=False)
    paid        = Column(Boolean, default=False)
    customer    = relationship("Customer", back_populates="payments")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)