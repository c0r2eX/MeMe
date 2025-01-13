
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import  Memeupload,  Register, Login 
from os import path
from uuid import uuid4
from ext import nag, db 
from modelebi import Meme , User , Vote
from flask_login import login_user , logout_user , current_user , login_required


users = {
    "Dachi": {"name": "Dachi", "age": 38, "role": "Admin", "gender": "Male", "image": "drak.jpg"},
    "Dato": {"name": "Dato", "age": 33, "role": "User", "gender": "Male", "image": "ishowspeed.jpg"},
    "Data": {"name": "Data", "age": 31, "role": "Moderator", "gender": "Male", "image": "kai cenat.jpg"},
}

# Memes = [
  #  {"img": "that-feeling-when-knee-surgery-is-tomorrow-v0-oe0jwdyzy4zd1.webp", "text": "knee surgery 100%"},
   # {"img": "canceled.jpg", "text": "knee surgery 0%"},
    #{"img": "gum-gun.jpg", "text": "avg american highschool"},
    #{"video": "tf2-tf2meme.mp4", "text": "Relatable"},
#]

@nag.route("/")
def index():
    Memebi = Meme.query.all()
    return render_template("main.html", memes=Memebi)



@nag.route("/register", methods=["GET", "POST"])
def register():
    form = Register()

    if form.validate_on_submit():
       
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username is already taken. Please choose a different one.", category="error")
        else:
            
            new_user = User(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("User registered successfully!", category="success")
            return redirect(url_for("index"))
    else:
        print("Form errors:")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")

    return render_template("register.html", form=form)

    

    return render_template("register.html", form=form)


@nag.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    
    if form.validate_on_submit():
      user = User.query.filter(User.username == form.username.data).first()
      if user != None and user.check_password(form.password.data):
          login_user(user)
          return redirect ("/")
          
    return render_template("login.html", form=form)

@nag.route("/logout")
def logout():
    logout_user()
    return redirect("/")
    

@nag.route("/profile/<username>")
def profile(username):
    user = users.get(username)
    if user is None:
        return render_template("dynamic.html")
    return render_template("dynamic.html", found_user=user)

@nag.route("/profilelist")
def profilelist():
    return render_template("profile_list.html", users=users)

@nag.route("/aboutme")
def aboutme():
    return render_template("aboutme.html")

@nag.route("/createpost", methods=["GET", "POST"])
@login_required
def create():
    form = Memeupload()

    if form.validate_on_submit():
        file = form.img.data
        filename, filetype = path.splitext(file.filename)
        filename = uuid4()
        filepath = path.join(nag.root_path, "static", f"{filename}{filetype}")
        file.save(filepath)

      
        new_meme = Meme(
            text=form.text.data,
            img=f"{filename}{filetype}",
            text_color=form.text_color.data,
        )
        db.session.add(new_meme)
        db.session.commit()

        flash("Meme uploaded successfully!", category="success")
        return redirect(url_for("index"))
    return render_template("create.html", form=form)


@nag.route("/editpost/<int:meme_id>", methods=["GET", "POST"])
def edit(meme_id):
    meme = Meme.query.get(meme_id)
    form = Memeupload(obj=meme)

    if form.validate_on_submit():
        meme.text = form.text.data
        meme.img = form.img.data
        meme.text_color = form.text_color.data
        
      

        db.session.commit()
        flash("Meme updated successfully!", category="success")
        return redirect("/")

    return render_template("create.html", form=form, meme=meme)





@nag.route("/upvote/<int:meme_id>", methods=["POST"])
@login_required
def upvote(meme_id):
    meme = Meme.query.get(meme_id)
    existing_vote = Vote.query.filter_by(user_id=current_user.id, meme_id=meme_id, vote_type='upvote').first()
    if not existing_vote:
        new_vote = Vote(user_id=current_user.id, meme_id=meme_id, vote_type='upvote')
        db.session.add(new_vote)
        meme.upvotes += 1
        db.session.commit()
    return redirect(url_for("index"))

@nag.route("/downvote/<int:meme_id>", methods=["POST"])
@login_required
def downvote(meme_id):
    meme = Meme.query.get(meme_id)
    existing_vote = Vote.query.filter_by(user_id=current_user.id, meme_id=meme_id, vote_type='downvote').first()
    if not existing_vote:
        new_vote = Vote(user_id=current_user.id, meme_id=meme_id, vote_type='downvote')
        db.session.add(new_vote)
        meme.downvotes += 1
        db.session.commit()
    return redirect(url_for("index"))



@nag.route("/delete_product/<int:meme_id>", methods=["POST" , "GET"])
def delete_meme(meme_id):
    meme = Meme.query.get(meme_id)
    
    votes = Vote.query.filter_by(meme_id=meme_id).all()
    for vote in votes:
        db.session.delete(vote)
    
    if meme:
        db.session.delete(meme)
        db.session.commit()
        flash("Meme deleted successfully!", category="success")
    else:
        flash("Meme not found.", category="error")
    return redirect(url_for("index"))
