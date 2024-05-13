from app import db


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    illnesses = db.Column(db.ARRAY(db.Text))
    weight = db.Column(db.Numeric(5, 2))
    height = db.Column(db.Numeric(5, 2))
    location = db.Column(db.String(100))
    food_preferences = db.Column(db.ARRAY(db.Text))
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    def __repr__(self):
        return "<UserProfile %r>" % self.user_id
