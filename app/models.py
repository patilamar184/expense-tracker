from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # user or admin

    expenses = relationship("Expense", back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) # e.g. "Chai"
    amount = Column(Float) # e.g. 20.0
    category = Column(String) # e.g. "food", "travel"
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="expenses")