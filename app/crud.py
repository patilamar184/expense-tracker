from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import security

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=security.hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.dict(), owner_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_my_expenses(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.owner_id == user_id).all()

def get_all_expenses(db: Session):
    return db.query(models.Expense).all()