from flask import Flask
from .extensions import ma
from .models import db
from flask import Blueprint
from .blueprints.customer import customers_bp
from .blueprints.ticket import tickets_bp
from .blueprints.mechanic import mechanics_bp
from .blueprints.part import parts_bp
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .extensions import db, ma, limiter, cache
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SpaceDock"
    }
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)


    migrate = Migrate(app, db)

    #register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(swaggerui_blueprint, url_prefix= SWAGGER_URL)


    return app