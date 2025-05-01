from pydantic import BaseModel, ConfigDict
from app.schemas.basemodel_config import MyBaseModel

class CategoryCreate(MyBaseModel):
    name: str

class CategoryPublic(MyBaseModel):
    id: int
    name:str

class CategoryList(MyBaseModel):
    categories: list[CategoryPublic]



