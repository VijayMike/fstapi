from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

# Create FastAPI instance
app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Product model
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for response
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data to populate the database (runs once when starting the app)
def populate_sample_data():
    db = SessionLocal()
    # Check if database is empty
    if db.query(ProductDB).count() == 0:
        sample_products = [
            ProductDB(name="Laptop", description="High-performance laptop", price=999.99, category="Electronics"),
            ProductDB(name="Smartphone", description="Latest model smartphone", price=699.99, category="Electronics"),
            ProductDB(name="Desk Chair", description="Ergonomic office chair", price=199.99, category="Furniture"),
            ProductDB(name="Coffee Maker", description="Automatic coffee machine", price=89.99, category="Appliances"),
        ]
        db.add_all(sample_products)
        db.commit()
    db.close()

# Run sample data population
populate_sample_data()

# Get all products endpoint
@app.get("/products/", response_model=List[Product])
def get_products():
    db = next(get_db())
    products = db.query(ProductDB).all()
    return products

# Optional: Get single product by ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    db = next(get_db())
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/", response_model=List[Product])
def root():
    db = next(get_db())
    products = db.query(ProductDB).all()
    return products
