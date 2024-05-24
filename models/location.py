from app import db

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<Location %r>" % self.name
