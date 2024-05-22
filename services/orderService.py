from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from models.product import Product
from models.order import Order


def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            # Get all of the product_ids from the order_data products
            product_ids = [prod['id'] for prod in order_data['products']]
            product_query = select(Product).where(Product.id.in_(product_ids))
            products = session.execute(product_query).scalars().all()

            # Make sure all of the products exist and were queried
            if len(product_ids) != len(products):
                raise ValueError("One or more products do not exist")
            
            # Check that the customer_id is associated with a customer
            customer_id = order_data['customer_id']
            customer = session.get(Customer, customer_id)

            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")
            
            # Create a new order in the database
            new_order = Order(date=order_data['date'], customer_id=customer_id, products=products)
            session.add(new_order)
            session.commit()

        session.refresh(new_order)

        for product in new_order.products:
            session.refresh(product)

        return new_order
    
def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders