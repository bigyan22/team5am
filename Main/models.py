from Main import db, login_manager
from werkzeug.security import check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=False)
    phone = db.Column(db.String(length=10), nullable=False, unique=False)
    description = db.Column(db.String(), nullable=False, unique=False)
    



class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=500), nullable=False, unique=False)
    email = db.Column(db.String(length=60),nullable=False, unique=True)
    
    def check_password_correction(self, attempted_password):
        return check_password_hash(self.password, attempted_password)
    