from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    name:str
    brand: str
    price:int
    cost_price: float  # 🔒 dada sensible
    stock: int

class ProductCreate(SQLModel):
    name: str
    brand: str
    price: int
    cost_price: float
    stock: int


class ProductRead(SQLModel):
    id: int
    name: str
    brand: str
    price: int
    stock: int

class ProductPartialRead(SQLModel):
    name:str
    brand:str
    stock: int

class ProductNameChange(SQLModel):
    name:str

class ProductNameBrand(SQLModel):
    name:str
    brand: str