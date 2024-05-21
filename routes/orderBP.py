from flask import Blueprint
from controllers.orderController import save

order_blueprint = Blueprint('order_bp', __name__)

order_blueprint.route('/', methods=['POST'])(save)