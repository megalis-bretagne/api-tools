import json
from flask import jsonify
from flask_restx import Namespace, Resource
from models.models import PublicationOpenData
from utils import row2dict

statistiques = Namespace('statistiques', description='API Statistiques')

@statistiques.route("/publication_open_data")
#@api.doc(params={'table': 'Nom de la table'})
class Statistiques(Resource):
    @statistiques.response(200, 'Success', statistiques.model('publication_opendata', PublicationOpenData().model))
    def get(self):
        #STATS = ("select * from pastell.publication_open_data LIMIT 100;")
        #with db.engine.connect() as con:
        #    query = con.execute(STATS)
        #return sql_to_json(query)
        #result = PublicationOpenData.query.all()
        #result = db.session.query(PublicationOpenData).all()
        #result = PublicationOpenData.query.limit(100).all()
        page = 1
        size = 5
        result = PublicationOpenData.query.paginate(page=page, per_page=size)
        data = {'response':'success','total': result.total, 'page': page, 'size': size, 'items': json.loads(json.dumps([row2dict(r) for r in result]))}
        return jsonify(**data)

