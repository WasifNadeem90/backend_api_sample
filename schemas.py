from pydantic import BaseModel
from datetime import date


class CreateProduct(BaseModel):
    name: str
    price: float
    description: str
    category_id: int


class CreateSale(BaseModel):
    product_id: int
    quantity: int
    sale_date: date


class CreateInventory(BaseModel):
    product_id: int
    quantity: int


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category_id: int

    class Config:
        orm_mode = True


class Sale(BaseModel):
    id: int
    product_id: int
    quantity: int
    sale_date: date

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    id: int
    product_id: int
    quantity: int
    updated_at: date

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True