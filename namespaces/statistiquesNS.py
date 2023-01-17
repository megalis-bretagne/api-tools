import json
from flask import jsonify
from flask_restx import Namespace, Resource, reqparse
from models.models import PublicationOpenData
from utils import row2dict

statistiques = Namespace('statistiques', description='API Statistiques')

arguments_publication_open_data = reqparse.RequestParser()
arguments_publication_open_data.add_argument('pageIndex', type=int, help='index de la page, commence par 1', default=1)
arguments_publication_open_data.add_argument('pageSize', type=int, help='taille de la page', default=100)

@statistiques.route("/publication_open_data")
class Publication(Resource):
    @statistiques.expect(arguments_publication_open_data)
    @statistiques.response(200, 'Success', statistiques.model('publication_opendata', PublicationOpenData().model))
    #@oidc.accept_token(require_token=True, scopes_required=['openid'])
    def get(self):
        args = arguments_publication_open_data.parse_args()
        page = args['pageIndex']
        size = args['pageSize']
        result = PublicationOpenData.query.paginate(page=page, per_page=size)
        data = {'response':'success','total': result.total, 'page': page, 'size': size, 'items': json.loads(json.dumps([row2dict(r) for r in result]))}
        return jsonify(**data)

