from flask import Blueprint
from controllers.customerController import save, find_all, get_customer

customer_blueprint = Blueprint("customer_bp", __name__)

customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/<customer_id>', methods=['GET'])(get_customer)