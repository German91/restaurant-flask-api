from project import db


class Restaurant(db.Model):

    # Table name
    __tablename__ = 'restaurants'

    # Fields
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    # Constructor
    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id


    def json(self):
        return {
            'title': self.title,
            'description': self.description
            'user': user.json()
        }


    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter_by(title=title).first()


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
