from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

import models
from schemas import CreateProduct, CreateSale, CreateInventory, Product, Sale, Inventory, Category
from models import Product as ProductModel, Sale as SaleModel, Inventory as InventoryModel, Category as CategoryModel
from database import get_db, engine
from sqlalchemy import func
from datetime import datetime, date
from typing import List

from fastapi.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def root():
    return RedirectResponse('/docs')


# Create a product
@app.post("/products/", response_model=Product)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Retrieve all products
@app.get("/products/", response_model=List[Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return products


# Retrieve product by ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Create a sale
@app.post("/sales/", response_model=Sale)
def create_sale(sale: CreateSale, db: Session = Depends(get_db)):
    db_sale = SaleModel(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


# Retrieve sales data by date range
@app.get("/sales/", response_model=List[Sale])
def get_sales_by_date_range(
        start_date: date = Query(...),
        end_date: date = Query(...),
        db: Session = Depends(get_db)
):
    sales = db.query(SaleModel).filter(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date).all()
    return sales


# Analyze revenue for a specific interval (daily, weekly, monthly, annual)
@app.get("/sales/revenue/")
def analyze_revenue(interval: str, start_date: date, end_date: date, db: Session = Depends(get_db)):
    if interval == "daily":
        # Perform daily revenue analysis
        result = db.query(SaleModel.sale_date, func.sum(SaleModel.quantity * ProductModel.price).label("revenue")). \
            join(ProductModel). \
            filter(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date). \
            group_by(SaleModel.sale_date).all()
        return result

    elif interval == "weekly":
        # Perform weekly revenue analysis
        result = db.query(func.strftime("%Y-%m", SaleModel.sale_date).label("week"),
                          func.sum(SaleModel.quantity * ProductModel.price).label("revenue")). \
            join(ProductModel). \
            filter(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date). \
            group_by(func.strftime("%Y-%m", SaleModel.sale_date)).all()
        return result

    elif interval == "monthly":
        # Perform monthly revenue analysis
        result = db.query(func.strftime("%Y-%m", SaleModel.sale_date).label("month"),
                          func.sum(SaleModel.quantity * ProductModel.price).label("revenue")). \
            join(ProductModel). \
            filter(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date). \
            group_by(func.strftime("%Y-%m", SaleModel.sale_date)).all()
        return result

    elif interval == "annual":
        # Perform annual revenue analysis
        result = db.query(func.strftime("%Y-%m", SaleModel.sale_date).label("year"),
                          func.sum(SaleModel.quantity * ProductModel.price).label("revenue")). \
            join(ProductModel). \
            filter(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date). \
            group_by(func.strftime("%Y-%m", SaleModel.sale_date)).all()
        return result

    else:
        raise HTTPException(status_code=400, detail="Invalid interval")


# Create inventory
@app.post("/inventory/", response_model=Inventory)
def create_inventory(inventory: CreateInventory, db: Session = Depends(get_db)):
    db_inventory = InventoryModel(**inventory.dict())
    db_inventory.updated_at = datetime.utcnow()
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# Retrieve current inventory status for a specific product
@app.get("/inventory/{product_id}", response_model=Inventory)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


# Update inventory levels for a specific product
@app.put("/inventory/{product_id}", response_model=Inventory)
def update_inventory(product_id: int, inventory: CreateInventory, db: Session = Depends(get_db)):
    db_inventory = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # Update inventory quantity
    db_inventory.quantity = inventory.quantity
    db_inventory.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# Get low stock alerts
@app.get("/inventory/low-stock/", response_model=List[Product])
def get_low_stock_alerts(threshold: int = Query(10), db: Session = Depends(get_db)):
    low_stock_products = db.query(ProductModel).join(InventoryModel).filter(InventoryModel.quantity < threshold).all()
    return low_stock_products
