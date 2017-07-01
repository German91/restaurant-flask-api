from project import app, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property


class User(db.Model):
    # Table name
    __tablename__ = 'users'

    # Fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Integer, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)

    # Relationships
    restaurants = db.Column(db.relationship('Restaurant', lazy='dynamic'))

    # Constructor
    def __init__(self, username, plaintext_password):
        self.username = username
        self.password = plaintext_password


    @hybrid_property
    def password(self):
        return self._password


    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)


    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)


    def json(self):
        return {
            'username': self.username,
            'restaurants': [restaurant.json() for restaurant in self.restaurants.all()]
        }


    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
