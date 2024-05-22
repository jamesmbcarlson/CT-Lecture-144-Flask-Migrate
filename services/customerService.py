from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from circuitbreaker import circuit
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token

# Fallback function - executed once the limit has been passed
def fallback_func(customer):
    print('The fallback function is being executed')
    return None

# Create a function that takes in customer data and creates a new customer
# @circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_func)
# def save(customer_data):
#     try:
#         if customer_data['name'] == 'Failure':
#             raise Exception("Failure condition triggered") # Raise an exception to simulate failure

#         # open a session
#         with Session(db.engine) as session:
#             with session.begin():
#                 # create a new instance of Customer
#                 new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], username=customer_data['username'], password=generate_password_hash(customer_data['password']))
#                 # Add and commit to the database
#                 session.add(new_customer)
#                 session.commit()
#             # After committing the session, the new_customer object may have become detached
#             # Refresh the object to ensure it is still attached to the session
#             session.refresh(new_customer)
#             return new_customer
#     except Exception as e:
#         # if an exception occurs, the circuit breaker will handle it based on configuration
#         raise e

# Create a function that takes in customer data and creates a new customer in db
def save(customer_data):
    # open a session
    with Session(db.engine) as session:
        with session.begin():
            # check to see if any user has that username
            customer_query = select(Customer).where(Customer.username == customer_data['username'])
            customer_check = db.session.execute(customer_query).scalars().first()
            if customer_check:
                raise ValueError("Customer with that username already exists")
            # create a new instance of Customer
            new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], username=customer_data['username'], password=generate_password_hash(customer_data['password']))
            # Add and commit to the database
            session.add(new_customer)
            session.commit()
        # After committing the session, the new_customer object may have become detached
        # Refresh the object to ensure it is still attached to the session
        session.refresh(new_customer)
        return new_customer
    
    
# Function to get all of the customer from the db
def find_all():
    query = db.select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers

# Function that will take in a username and password and return token if valid, None if not
def get_token(username, password):
    # Query the customer table for that username
    query = db.select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalars().first()
    if customer is not None and check_password_hash(customer.password, password):
        # Create a token with the customer's id
        auth_token = encode_token(customer.id)
        # resp = {
        #     "status": "success",
        #     "message": "successfully logged in",
        #     "token": auth_token
        # }
        auth_token = encode_token(customer.id)
        return auth_token
    else:
        return None