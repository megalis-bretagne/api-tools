from flask_sqlalchemy import SQLAlchemy
from flask_restx import fields

db = SQLAlchemy()

class PublicationOpenData(db.Model):
    __tablename__ = 'publication_open_data'
    __table_args__ = {"schema":"pastell"}
    id_d = db.Column(db.String(10), primary_key=True)
    id_e = db.Column(db.String(10))
    date_action = db.Column(db.Date())
    acte_nature = db.Column(db.String(2))
    rejeu = db.Column(db.Boolean())
    publication_opendata = db.Column(db.Boolean())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_d': self.id_d,
            'id_e': self.id_e,
            'date_action': self.date_action
        }
    @property
    # USed by api flask_restx
    def model(self):
        return {
            'id_d': fields.String,
            'id_e': fields.String,
            'date_action': fields.Date,
            'acte_nature': fields.String,
            'rejeu': fields.Boolean,
            'publication_opendata': fields.Boolean,
            'toto': fields.String
        }

class Organigramme(db.Model):
    __tablename__ = 'organigramme'
    __table_args__ = {"schema":"pastell"}
    id_e = db.Column(db.String(10), primary_key=True)
    level = db.Column(db.String(2))
    entite_mere = db.Column(db.String(10))
    path = db.Column(db.String(512))
    code = db.Column(db.String(256))
    siren = db.Column(db.String(12))
    date_inscription = db.Column(db.String(25))
    is_active = db.Column(db.String(2))
    denomination = db.Column(db.String(256))

    @property
    # USed by api flask_restx
    def model(self):
        return {
            'id_e': fields.String,
            'level': fields.String,
            'entite_mere': fields.String,
            'path': fields.String,
            'code': fields.String,
            'date_inscription': fields.String,
            'is_active': fields.String,
            'denomination': fields.String
        }

