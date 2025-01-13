

from ext import nag, db
from routes import index, register, login, logout, profile, profilelist, aboutme, create, edit, upvote, downvote, delete_meme


nag.run(host="0.0.0.0", debug=True)
