from flask_login import LoginManager , UserMixin
from ext import db , login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    img = db.Column(db.String(), nullable=True)
    text_color = db.Column(db.String(7), nullable=False, default="#000000")  
    upvotes = db.Column(db.Integer, default=0)  
    downvotes = db.Column(db.Integer, default=0)  
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))        
    password = db.Column(db.String(25))
   
   
    def __init__(self , username, password):
        self.username = username
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def save():
        db.session.commit()
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meme_id = db.Column(db.Integer, db.ForeignKey('meme.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  
    

    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    meme = db.relationship('Meme', backref=db.backref('votes', lazy=True))

    def __repr__(self):
        return f"<Vote user={self.user_id} meme={self.meme_id} type={self.vote_type}>"




class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meme_id = db.Column(db.Integer, db.ForeignKey('meme.id'), nullable=False)

    user = db.relationship('User', backref='comments')
    meme = db.relationship('Meme', backref='comments')
