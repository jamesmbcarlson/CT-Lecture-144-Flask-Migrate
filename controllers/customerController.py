from flask import request, jsonify
from schemas.customerSchema import customer_input_schema, customer_output_schema, customers_schema, customer_login_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache

def save():
    try:
        # Validate and deserialize the request data
        customer_data = customer_input_schema.load(request.json)
        customer_save = customerService.save(customer_data)
        return customer_output_schema.jsonify(customer_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    
    # Call the save service with the customer data
    # customer_save = customerService.save(customer_data)
    # # Check to see that the customer_save is a customer and not None
    # if customer_save is not None:
    #     # Serialize the customer data and return with a 201 success
    #     return customer_output_schema.jsonify(customer_save), 201
    # else:
    #     return jsonify({"message": "Fallback method error activated", "body": customer_data}), 400
    
@cache.cached(timeout=60)
def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200
    
def get_token():
    try:
        customer_data = customer_login_schema.load(request.json)
        token = customerService.get_token(customer_data['username'], customer_data['password'])
        if token:
            resp = {
                "status": "success",
                "message": "You have successfully authenticated yourself",
                "token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401 # 401 - HTTP Status - Unauthorized
    except ValidationError as err:
        return jsonify(err.messages), 400
    