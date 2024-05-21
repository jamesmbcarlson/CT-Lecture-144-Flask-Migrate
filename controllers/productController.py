from flask import request, jsonify
from schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError

def save():
    try:
        # Validate and deserialize the request data
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = productService.save(product_data)
    
    return product_schema.jsonify(new_product), 201

def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200