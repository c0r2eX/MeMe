from ext import nag, db
from modelebi import Meme , User , Comment

with nag.app_context():
    
    
    db.create_all()
