from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from database import db, migrate
from schemas import ma
from limiter import limiter
from caching import cache

# VS Code says not access, but apparently these are what are creating our tables? <-- I'm not conviced, just because I took these out of a similar homework assignment and the tables were still created
# okay, I just tested it out; customer's get created elsewhere, but the other two, at the time of writing this note, only have a model (no controllers, schema, etc) so they're initialized as empty tables, with the expected columns
from models.customer import Customer
# from models.customerAccount import CustomerAccount
from models.product import Product
from models.order import Order
from models.orderProduct import order_product
from models.role import Role

from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.tokenBP import token_blueprint


SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI
API_URL = '/static/swagger.yaml' # Pth to the YAML file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'CT E-Commerce'}
)


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    blueprint_config(app)
    config_rate_limit()

    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(token_blueprint, url_prefix='/token')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def config_rate_limit():
    limiter.limit("100 per hour")(customer_blueprint)
    limiter.limit("100 per hour")(product_blueprint)

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')

    

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
        
    app.run(debug=True) # Brian set his port here; e.g, port=8888