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

