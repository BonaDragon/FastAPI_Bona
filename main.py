from fastapi import FastAPI
app = FastAPI()

users = [
    {"id": 1, "nombre": "Juan", "apellido":"Gonzalez", "edad": 30},
    {"id": 2, "nombre": "Ana" , "apellido":"Perez", "edad": 22},
    {"id": 3, "nombre": "Luis" ,"apellido":"Martinez", "edad": 21}
]

@app.get("/api/users/{user_id}")
def find_user(user_id: int):

     for user in users:
         if user["id"] == user_id:
            return user
     return "User not found"


@app.get("/api/users")
def list_users():

    return users


@app.post("/api/users")
def create_user(name : str, surname: str, age : int):

    users.append({"id":len(users) +1, "nombre": name , "apellido": surname, "edad": age})
    return users

@app.put("/api/users/{user_id}")
def update_user(user_id: int, name:str, surname:str,age:int):

     for user in users:
         if user["id"] == user_id:
             user["nombre"] = name
             user["apellido"] = surname
             user["edad"] = age
             return user
     return "User not found"

@app.patch("/api/users/{user_id}")
def update_name_age(user_id: int, name:str, age:int):

     for user in users:
         if user["id"] == user_id:
             user["nombre"] = name
             user["edad"] = age
             return user
     return "User not found"

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):

     for user in users:
         if user["id"] == user_id:

            users.remove(user)

     return users
