from flask import request, jsonify
from schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache

def save():
    try:
        # Validate and deserialize the request data
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Call the save service with the customer data
    customer_save = customerService.save(customer_data)
    # Check to see that the customer_save is a customer and not None
    if customer_save is not None:
        # Serialize the customer data and return with a 201 success
        return customer_schema.jsonify(customer_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": customer_data}), 400
    
@cache.cached(timeout=60)
def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200
    