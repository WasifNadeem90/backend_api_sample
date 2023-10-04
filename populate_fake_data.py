import random
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Product, Sale, Inventory, Category

from database import get_db

fake = Faker()


def generate_fake_categories(session: Session, num_categories: int):
    for _ in range(num_categories):
        category = Category(
            name=fake.unique.color()
        )
        session.add(category)
    session.commit()


def generate_fake_products(session: Session, num_products: int):
    categories = session.query(Category).all()
    for _ in range(num_products):
        category = random.choice(categories)
        product = Product(
            name=fake.unique.first_name(),
            price=random.uniform(10.0, 100.0),
            description=fake.text(),
            category_id=category.id,
        )
        session.add(product)
    session.commit()


def generate_fake_sales(session: Session, num_sales: int):
    products = session.query(Product).all()
    print(f"Number of products: {len(products)}")  # Debugging line
    for _ in range(num_sales):
        product = random.choice(products)
        sale_date = fake.date_between(start_date='-30d', end_date='today')
        sale = Sale(
            product_id=product.id,
            quantity=random.randint(1, 10),
            sale_date=sale_date,
        )
        session.add(sale)


def generate_fake_inventory(session: Session, num_inventory_items: int):
    products = session.query(Product).all()
    print(f"Number of products: {len(products)}")  # Debugging line
    for _ in range(num_inventory_items):
        product = random.choice(products)
        inventory = Inventory(
            product_id=product.id,
            quantity=random.randint(10, 100),
            updated_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        session.add(inventory)


db = next(get_db())
try:
    # Adjust the number of products, sales, and inventory items as needed
    num_products = 50
    num_sales = 100
    num_inventory_items = 50
    num_categories = 10

    generate_fake_categories(db, num_categories)
    generate_fake_products(db, num_products)
    generate_fake_sales(db, num_sales)
    generate_fake_inventory(db, num_inventory_items)

    db.commit()
finally:
    db.close()
