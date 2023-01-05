import os, json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, request, Blueprint, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Resource, Api
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, version='0.1', title='Tools Api', description='API PRAE Tools', doc='/docs/')
app.register_blueprint(blueprint)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)



url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)

date_oid = 1082 # id of date type, see docs how to get it from db
def casting_fn(val,cur):
  # process as you like, e.g. string formatting
    # register custom mapping
    datetype_casted = psycopg2.extensions.new_type((date_oid,), "date", casting_fn)
    psycopg2.extensions.register_type(datetype_casted)

statistiques = api.namespace('statistiques', description='API Statistiques')


@statistiques.route("/<string:table>")
@api.doc(params={'table': 'Nom de la table'})
class Statistiques(Resource):
    def get(self, table):
        STATS = (f"select * from pastell.{table};")
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(STATS)
                results = cursor.fetchall()
                results = json.loads(json.dumps(results, cls=DateEncoder))
        return results, 200

if __name__ == "__main__":
    app.run(host='127.0.0.1')
