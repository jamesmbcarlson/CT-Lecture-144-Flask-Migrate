from marshmallow import fields
from schemas import ma


class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.Nested("ProductIdSchema", many=True)
    
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
