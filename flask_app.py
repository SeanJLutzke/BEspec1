from application import create_app
from application.extensions import db
from flask_migrate import Migrate
from application.models import Customer
from sqlalchemy import inspect


app = create_app('ProductionConfig')
migrate = Migrate(app, db)
#things won't work if I don't migrate the database
with app.app_context():
    db.create_all()


#Initialization
#app = Flask(__name__)

#config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootuser@localhost/ecommerce_api'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# WINDOWS KEY + R
# search "services.msc"
# find MySQL84
# right click it 
# open MySQL


#.\venv\Scripts\Activate    
# python app.py


#old startup stuff


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         #inspector = inspect(db.engine)
#         #print(inspector.get_table_names())
#     app.run(debug=True)


                        
