from issues_blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Helps the extension find the correct user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    issues = db.relationship('Issue', backref = 'author', lazy = True)

    def __repr__(self) -> str:
        return f"User('{self.firstname}', '{self.email}')"

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), nullable = False)
    content = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(20), nullable = False, default = 'Pending')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self) -> str:
        return f"Issue('{self.title}', '{self.date_created}')"