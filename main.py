from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Lista de usuarios
users = [
    {"id": 1, "nombre": "Juan", "surname": "Gonzalez", "edad": 30},
    {"id": 2, "nombre": "Ana", "surname": "Perez", "edad": 22},
    {"id": 3, "nombre": "Luis", "surname": "Martinez", "edad": 21}
]

class UserModel(BaseModel):
    id: int
    nombre: str
    surname: str
    edad: int

# Función para obtener el siguiente ID
def get_next_id():
    if not users:
        return 1
    max_id = max(user["id"] for user in users)
    return max_id + 1

# Función para devolver todos los usuarios en diccionario con pydantic V2(BaseModel)
def list_all():
    return [UserModel(**user).model_dump() for user in users]

# Endpoints
@app.get("/api/users/{user_id}", response_model=dict)
def find_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return UserModel(**user).model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/users", response_model=dict)
def list_users():
    return {"users": list_all()}

@app.post("/api/users", response_model=dict)
def create_user(name: str, surname: str, age: int):
    new_user = {"id": get_next_id(), "nombre": name, "surname": surname, "edad": age}
    users.append(new_user)
    return {"users": list_all()}

@app.put("/api/users/{user_id}", response_model=dict)
def update_user(user_id: int, name: str, surname: str, age: int):
    for user in users:
        if user["id"] == user_id:
            user["nombre"] = name
            user["surname"] = surname
            user["edad"] = age
            return {"users": list_all()}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/api/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"users": list_all()}
    raise HTTPException(status_code=404, detail="User not found")
