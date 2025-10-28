import os
from typing import List
from fastapi import FastAPI, Depends
from sqlmodel import create_engine, Session, SQLModel, select
from dotenv import load_dotenv
from FastAPI_Bona.models.product import Product, ProductCreate, ProductRead, ProductPartialRead, ProductNameChange, ProductNameBrand


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

#1.Ceate - Afegir un nou registre a la taula
@app.post("/api/user", response_model=dict)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product.model_validate(product)
    db.add(db_product)
    db.commit()
    return {"message": "Product created!"}


#2.Read - Consultar totes les dades d’un registre a la taula.
@app.get("/api/product/{id}", response_model=ProductRead)
def find_product(product_id: int, db: Session = Depends(get_db)):

    product = db.get(Product, product_id)

    return ProductRead.model_validate(product)

#3.Read - Consultar totes les dades de tots els registres de la taula.
@app.get("/api/products/",  response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):

    product = db.exec(select(Product)).all()
    return product

#4.Read - Consultar les dades filtrant per un camp
@app.get("/api/products/{filter}",  response_model=List[ProductRead])
def list_products_by_higher_price(value:int ,db: Session = Depends(get_db)):
    #selecciona productos que sean de un precio mayor al seleccionado
    stmt = select(Product).where(Product.price > value)
    product = db.exec(stmt).all()
    return product


#5.Delete - Eliminar un registre per id
@app.delete("/api/product/{id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    db.delete(product)
    db.commit()
    return {"message": "Product have been deleted!"}

#6.Read - Lectura parcial

@app.get("/api/product/partial/{id}", response_model=ProductPartialRead)
def find_product_partial_data(product_id: int, db: Session = Depends(get_db)):

    product = db.get(Product, product_id)

    return ProductPartialRead.model_validate(product)


#7.Update - Modificació total (PUT)

@app.put("/api/product/update/{product_id}", response_model= ProductCreate)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.get(Product, product_id)
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    db.add(db_product)
    db.commit()
    return ProductCreate.model_validate(db_product)


#8.Update - Modificació parcial un camp (PATCH)
@app.patch("/api/product/{product_id}", response_model = ProductNameChange)
def update_name(product_id: int, product: ProductNameChange, db: Session = Depends(get_db)):
    db_product = db.get(Product, product_id)
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    db.add(db_product)
    db.commit()
    return ProductNameChange.model_validate(db_product)

#9.Update - Modificació parcial dos camps
@app.patch("/api/product/name&brand/{product_id}", response_model = ProductNameBrand)
def update_name_brand(product_id: int, product: ProductNameBrand, db: Session = Depends(get_db)):
    db_product = db.get(Product, product_id)
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    db.add(db_product)
    db.commit()
    return ProductNameBrand.model_validate(db_product)