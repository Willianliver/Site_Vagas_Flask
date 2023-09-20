from werkzeug.utils import secure_filename
from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime
import os

from app.models.tables import User, Post
from app.models.forms import LoginForm, RegisterForm, PostForm


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/vagas/",methods=['GET', 'POST'])
def index():
    form_post = PostForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.date.desc()).all()
            return render_template('index.html', form=form_post, posts=posts)
        else:
            return redirect(url_for("login"))

    else:
        if form_post.validate_on_submit():
            id = current_user.get_id()
            user = User.query.filter_by(id=id).first()
            date = datetime.now().strftime('%d/%m/%Y %H:%M')
            NewPost = Post(content=form_post.content.data, title=form_post.title.data, date=date, user=user.name,
                           nick=user.username, user_id=id, vaga=form_post.vaga.data, salario=form_post.salario.data,
                           contato=form_post.contato.data)
            db.session.add(NewPost)
            db.session.commit()
            print(NewPost)
            return redirect(url_for("index"))
        else:
            return "ERRO!!"


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            return redirect(url_for("index"))
        else:
            flash("Invalid login.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            NewUserData = User(form.username.data, form.password.data, form.name.data, form.email.data)
            print(NewUserData)
            db.session.add(NewUserData)
            db.session.commit()
            return redirect(url_for("login"))
        except:
            return redirect(url_for("register"))
    else:
        print(form.errors)
    return render_template('register.html', form=form)


@app.route('/profile/<int:id>/')
def profile(id):
    if current_user.id == id:
        return redirect(url_for("my_profile"))
    else:
        posts = Post.query.filter_by(user_id=id).order_by(Post.date.desc()).all()
        user = User.query.filter_by(id=id).first()
        try:
            print(user.id)
            if user.id != False:
                print('pagina do perfil ' + str(id))
                return render_template('profile.html', posts=posts, profile=user)
        except:
            return redirect(url_for("my_profile"))


@app.route('/profile/')
def my_profile():
    if current_user.is_authenticated == True:
        user = User.query.filter_by(id=current_user.id).first()
        posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.date.desc()).all()
        return render_template('my_profile.html', profile=user, posts=posts)
    else:
        redirect(url_for("login"))


def change_profile_pic_name(name):
    date = datetime.now().strftime('%d%m%Y%H%M%S')
    old_name = name.split(".")
    old_name[0] = "profile_pic" + str(date)
    new_name = '.'.join(old_name)
    return new_name


@app.route('/profile/change_image', methods=['POST'])
def profile_image():
    UPLOAD_FOLDER = os.path.join(os.getcwd(), str('app/static/images/' + str(current_user.get_id())))
    if UPLOAD_FOLDER == True:
        os.mkdir(UPLOAD_FOLDER)
    file = request.files['image']
    file.filename = change_profile_pic_name(file.filename)
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)
    prof = User.query.filter_by(id=current_user.get_id()).first()
    prof.pic = str("/static/images/" + str(current_user.get_id()) + '/' + str(file.filename))
    db.session.add(prof)
    db.session.commit()
    print(prof.pic)
    return redirect(url_for("my_profile"))


@app.route('/search', methods=['POST'])
def search():
    search_data = request.form.get("search_data")
    search = "%{}%".format(search_data)
    posts = Post.query.filter(Post.title.like(search)).all()
    users = User.query.filter(User.name.like(search)).all()
    return render_template('search.html', users=users, posts=posts, search=search_data)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    id = request.form.get("id")
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newcontent = request.form.get("newcontent")
    oldcontent = request.form.get("oldcontent")
    newvaga = request.form.get("newvaga")
    oldvaga = request.form.get("oldvaga")
    newsalario = request.form.get("newsalario")
    oldsalario = request.form.get("oldsalario")
    newcontato= request.form.get("newcontato")
    oldcontato = request.form.get("oldcontato")
    post = Post.query.filter_by(title=oldtitle, content=oldcontent, vaga=oldvaga, salario=oldsalario, contato=oldcontato).first()
    post.title = newtitle
    post.content = newcontent
    post.vaga = newvaga
    post.salario = newsalario
    post.contato = newcontato
    db.session.commit()
    return redirect("/")

'''
def deletarpessoa(id):
    if db.search(Post.id==id):
        db.remove(Post.id==id)
    else:
        print("usuario não encontrado")
'''




'''
@app.route('/delete/<int:id>', methods=['GET','POST','DELETE'])
def delete(id):
    try:
        deletarpessoa(id)
        return redirect("/profile")
    except:
        return "erro"


 if request.method == 'DELETE':
        if current_user.id == id:
            id = request.form.get("id")
            post = Post.query.filter_by(id=id).first()
            db.session.delete(post)
            db.session.commit()
    return redirect("/profile")
'''

