import os
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, Session, SQLModel, select
from dotenv import load_dotenv
from FastAPI_Bona.models.product import Product, ProductCreate, ProductRead


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

#Ceate - Afegir un nou registre a la taula
@app.post("/api/user", response_model=dict)
def create_product(user: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product.model_validate(user)
    db.add(db_product)
    db.commit()
    return {"message": "Product created!"}


#Read - Consultar totes les dades d’un registre a la taula.
@app.get("/api/product/{id}", response_model=ProductRead)
def find_product(product_id: int, db: Session = Depends(get_db)):

    product = db.get(Product, product_id)

    return ProductRead.model_validate(product)

#Read - Consultar totes les dades de tots els registres de la taula.
@app.get("/api/products/",  response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):

    product = db.exec(select(Product)).all()
    return product

#Read - Consultar les dades filtrant per un camp
@app.get("/api/products/{filter}",  response_model=List[ProductRead])
def list_products_by_higher_price(value:str ,db: Session = Depends(get_db)):
    #selecciona productos que sean de un precio mayor al seleccionado
    stmt = select(Product).where(Product.price > value)
    product = db.exec(stmt).all()
    return product


#Delete - Eliminar un registre per id
@app.delete("/api/product/{id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    db.delete(product)
    db.commit()
    return {"message": "Product have been deleted!"}