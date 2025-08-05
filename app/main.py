from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, auth, expenses, category, monthly_income, insights


app = FastAPI(title="Managment ExpensesAPI", version="0.0.2")

origins = [
    "https://gerenciador-despesas-frontend.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(monthly_income.router, prefix="/api")
app.include_router(insights.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "API ONLINE"}
