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



                        
