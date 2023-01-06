import os, json
from dotenv import load_dotenv
from flask import Flask, request, Blueprint, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Resource, Api, fields
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

load_dotenv()  # loads variables from .env file into environment

db = SQLAlchemy()
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, version='0.1', title='Tools Api', description='API PRAE Tools', doc='/docs/')
app.register_blueprint(blueprint)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


url = os.environ.get("DATABASE_URL")  # gets variables from environment
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = url
# initialize the app with the extension
db.init_app(app)


class PublicationOpenData(db.Model):
    __tablename__ = 'publication_open_data'
    __table_args__ = {"schema":"pastell"}
    id_d = db.Column(db.String(10), primary_key=True)
    id_e = db.Column(db.String(10))
    date_action = db.Column(db.Date())
    acte_nature = db.Column(db.String(2))
    rejeu = db.Column(db.Boolean())
    publication_opendata = db.Column(db.Boolean())


model_publication_opendata = api.model('publication_opendata', {
    'id_d': fields.String,
    'id_e': fields.String,
    'date_action': fields.Date,
    'acte_nature': fields.String,
    'rejeu': fields.Boolean,
    'publication_opendata': fields.Boolean
})


statistiques = api.namespace('statistiques', description='API Statistiques')


@statistiques.route("/publication_open_data")
#@api.doc(params={'table': 'Nom de la table'})
class Statistiques(Resource):
    @api.response(200, 'Success', model_publication_opendata)
    def get(self):
        STATS = ("select * from pastell.publication_open_data LIMIT 100;")
        with db.engine.connect() as con:
            query = con.execute(STATS)

        return sql_to_json(query)


def sql_to_json(query):
    rows = query.fetchall()
    fields = query.keys()
    object_list = []
    for row in rows:
        json_row = {}
        fields = [f for f in query.keys()]
        for field in fields:
            index = fields.index(field)
            json_row[field] = row[index]
        object_list.append(json_row)
    return jsonify(object_list)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
