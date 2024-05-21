from flask import request, jsonify
from schemas.orderSchema import order_schema
from marshmallow import ValidationError
from services import orderService


def save():
    try:
        order_data = order_schema.load(request.json)
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400



