from flask import Flask
from .extensions import ma
from .models import db
from flask import Blueprint
from .blueprints.customer import customers_bp
from .blueprints.ticket import tickets_bp
from .blueprints.mechanic import mechanics_bp
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
#part 1 ^^^^^^
from .extensions import db, ma, limiter, cache


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


    return app