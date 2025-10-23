import os
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from FastAPI_Bona.models.user import User, UserCreate, UserRead


app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

#DB connect
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()



# Endpoints
@app.get("/api/user/{user_id}", response_model=UserRead)
def find_user(user_id: int, db: Session = Depends(get_db)):
    # Construir la consulta SQL
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)

@app.post("/api/user", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    return db_user
