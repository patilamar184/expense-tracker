from pydantic import BaseModel

# --- Auth ---
class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Expense ---
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    owner_id: int
    class Config:
        from_attributes = True