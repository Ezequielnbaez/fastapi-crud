from database import Base
from sqlalchemy import Column, Integer, String, Float

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    category = Column(String)
    description = Column(String)
    stock = Column(Integer)

