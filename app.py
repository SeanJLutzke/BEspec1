from application import create_app
from application.models import db
from flask_migrate import Migrate



app = create_app('DevelopmentConfig')


#Initialization
#app = Flask(__name__)

#config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootuser@localhost/ecommerce_api'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# "load-bearing coconut"
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# WINDOWS KEY + R
# search "services.msc"
# find MySQL84
# right click it 
# open MySQL


#.\venv\Scripts\Activate    
# python app.py


# Hey Sean, you’re on the right track! There are just a few areas we need to polish before it can pass:

# File organization: Some folders are empty, and there are extra __init__.py files that aren’t needed.

# Dependencies: We’re missing a requirements.txt. This is important to avoid version conflicts with the packages.

# Database setup: Your code isn’t creating the necessary tables, so none of the functions are working. Make sure 
# the tables are being created properly according to your functions.



                        
