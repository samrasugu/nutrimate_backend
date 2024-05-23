from app import db

class Disease(db.Model):
    __tablename__ = "diseases"

    disease_id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<Disease %r>" % self.disease_name
