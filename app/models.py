from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    postcontents = db.relationship('PostContent', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model): #Göra lista med alla posts i denna för detta ska vara en post som innehåller posts
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    # body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(64))

    def __repr__(self):
        return '<Post {}>'.format(self.title)

#Lol så vanliga post var förrrr att ha lol vilka 
class PostContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer) #Vilken som lol är parent posten till denna. Ska automatiskt bli denna, ska inte behöva manuellt. När går in på en post så kommer det vara en såhär add to collections, och då det blir form för att lägga till saker mitt namn är jeff. Då kommer automatiskt den post man är storas som parent lolllllllllllllllllllllllllllllllllllllllll.
    title = db.Column(db.String(64))
    description = db.Column(db.String(140))
    # body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #ksk inte ska ha timestamp på vanlig post, bara på denna lol
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(64))

    def __repr__(self):
        return '<PostContent {}>'.format(self.title)
