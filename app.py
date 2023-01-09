import os
from dotenv import load_dotenv
from flask import Flask, request, Blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api

from models.models import db
from namespaces.statistiquesNS import statistiques

#loads variables from .env file into environment
load_dotenv()

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, version='0.1', title='Tools Api', description='API PRAE Tools', doc='/docs/')
app.register_blueprint(blueprint)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

#Add API namespaces
api.add_namespace(statistiques)

# configure the POSGRESQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

# initialize the app with the database
db.init_app(app)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
