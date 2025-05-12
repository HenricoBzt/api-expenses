from app.schemas.basemodel_config import MyBaseModel

class ExpenseClassifierRequest(MyBaseModel):
    description: str

class ExpenseClassifierResponse(MyBaseModel):
    suggested_category: str

