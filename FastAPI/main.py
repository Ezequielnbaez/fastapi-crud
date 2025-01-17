from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated,List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ProductBase(BaseModel):
    price: float
    category: str
    description:str
    stock: int

class ProductModel(ProductBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


#ENDPOINT
@app.post("/products/", response_model=ProductModel)
async def create_product(product: ProductBase, db: db_dependency):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
async def read_products(db: db_dependency, skip: int= 0, limit:int=100):
    products=db.query(models.Product).offset(skip).limit(limit).all()
    return products