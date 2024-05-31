from flask import request, jsonify
from schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from auth import token_auth


@token_auth.login_required(role="admin")
def save():
    try:
        # Validate and deserialize the request data
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = productService.save(product_data)
    
    return product_schema.jsonify(new_product), 201

def find_all():
    # Get any request query params aka args
    args = request.args
    page = args.get('page', 1, type=int)
    # print('The page arg is:', page, 'and the type is', type(page))
    per_page = args.get('per_page', 10, type=int)
    search_term = args.get('search')
    products = productService.find_all(page, per_page, search_term)
    return products_schema.jsonify(products), 200