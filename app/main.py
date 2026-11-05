from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas, crud
from app.auth import security
from app.auth.dependencies import get_current_user, get_admin_user

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Mini Expense Tracker")

# --- AUTH ROUTES ---
@app.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    return crud.create_user(db, user)

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Wrong email or password")
    
    token = security.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
def me(current_user: models.User = Depends(get_current_user)):
    return {"email": current_user.email, "role": current_user.role}

# --- EXPENSE ROUTES ---
@app.post("/expenses", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Authorization: This expense will be saved with MY id
    return crud.create_expense(db, expense, current_user.id)

@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def my_expenses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_my_expenses(db, current_user.id)

@app.get("/expenses/all", response_model=list[schemas.ExpenseResponse])
def all_expenses(db: Session = Depends(get_db), admin: models.User = Depends(get_admin_user)):
    # Only admin can hit this
    return crud.get_all_expenses(db)

@app.get("/expenses/total")
def my_total(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    expenses = crud.get_my_expenses(db, current_user.id)
    total = sum(e.amount for e in expenses)
    return {"email": current_user.email, "total_spent": total}