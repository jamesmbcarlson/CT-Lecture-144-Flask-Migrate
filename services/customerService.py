from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from circuitbreaker import circuit

# Fallback function - executed once the limit has been passed
def fallback_func(customer):
    print('The fallback function is being executed')
    return None

# Create a function that takes in customer data and creates a new customer
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_func)
def save(customer_data):
    try:
        if customer_data['name'] == 'Failure':
            raise Exception("Failure condition triggered") # Raise an exception to simulate failure

        # open a session
        with Session(db.engine) as session:
            with session.begin():
                # create a new instance of Customer
                new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                # Add and commit to the database
                session.add(new_customer)
                session.commit()
            # After committing the session, the new_customer object may have become detached
            # Refresh the object to ensure it is still attached to the session
            session.refresh(new_customer)
            return new_customer
    except Exception as e:
        # if an exception occurs, the circuit breaker will handle it based on configuration
        raise e
    
    
# Function to get all of the customer from the db
def find_all():
    query = db.select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers