from fastapi import FastAPI
from http import HTTPStatus
from app.routes import users, auth,expenses, category, monthly_income, insights,expense_classifier


app = FastAPI( 
    title="Managment ExpensesAPI",
    version="0.0.2")

app.include_router(users.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(expenses.router, prefix='/api')
app.include_router(category.router, prefix='/api')
app.include_router(monthly_income.router,prefix='/api')
app.include_router(insights.router,prefix='/api')
app.include_router(expense_classifier.router,prefix='/api')

@app.get('/')
def read_root():
    return {'message': 'API ONLINE'}

