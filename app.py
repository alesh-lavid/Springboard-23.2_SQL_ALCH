"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home_rout():
    return redirect('/users')

@app.route('/users')
def users_rout():

    users = User.query.all()
    return render_template('templates/users.html', users=users)


@app.route("/users/new", methods=["POST"])
def new_user_rout():

    new_user = User(first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_id_rout(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('templates/user_show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit_rout(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('templates/user_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_rout(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_rout(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#################################

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('tempaltes/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_rout(user_id):

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post_rout(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('template/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('template/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def destroy_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")