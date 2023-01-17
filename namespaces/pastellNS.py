import json
from flask import jsonify
from flask_restx import Namespace, Resource, reqparse
from models.models import Organigramme
from utils import row2dict


pastell = Namespace('pastell', description='API Pastell')

arguments_organismes = reqparse.RequestParser()
arguments_organismes.add_argument('pageIndex', type=int, help='index de la page, commence par 1', default=1)
arguments_organismes.add_argument('pageSize', type=int, help='taille de la page', default=100)

@pastell.route("/organismes/")
@pastell.route("/organismes/<string:siren>")
class Organismes(Resource):
    @pastell.expect(arguments_organismes)
    @pastell.response(200, 'Success', pastell.model('organisme', Organigramme().model))
    #@oidc.accept_token(require_token=True, scopes_required=['openid'])
    def get(self, siren=None):
        args = arguments_organismes.parse_args()
        page = args['pageIndex']
        size = args['pageSize']
        if siren:
            result = Organigramme.query.filter(Organigramme.siren == siren, Organigramme.is_active == '1').paginate(page=page, per_page=size)
        else:
            result = Organigramme.query.paginate(page=page, per_page=size)
        data = {'response':'success','total': result.total, 'page': page, 'size': size, 'items': json.loads(json.dumps([row2dict(r) for r in result]))}
        return jsonify(**data)

