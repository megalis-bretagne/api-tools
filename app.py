import os, json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, request, Blueprint, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Resource, Api

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, version='0.1', title='Tools Api', description='API PRAE Tools', doc='/docs/')
app.register_blueprint(blueprint)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)



url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)

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
                jsonObj = json.dumps(results, indent=1, sort_keys=True, default=str)
                json.loads(jsonObj)

        return results, 200

if __name__ == "__main__":
    app.run(host='127.0.0.1')
