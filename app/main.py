from fastapi import FastAPI
from http import HTTPStatus
from app.routes import users, auth,expenses


app = FastAPI()

app.include_router(users.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(expenses.router, prefix='/api')


@app.get('/')
def read_root():
    return {'message': 'API ONLINE'}

