from pydantic import BaseModel, ConfigDict

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes= True
    )

class CategoryCreate(MyBaseModel):
    name: str

class CategoryPublic(MyBaseModel):
    id: int
    name:str

class CategoryList(MyBaseModel):
    categories: list[CategoryPublic]



