from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    firstname:str
    lastname: str
    age:int


#Modelo de creación de usuarios(entrada)
class UserCreate(SQLModel):
    firstname: str
    lastname: str
    age: int

# Modelo de salida (lo que se devuelve al cliente)
class UserRead(SQLModel):
    id: int
    firstname: str
    lastname: str
    age: int
