from flask import render_template, url_for, flash, redirect, request
from Main.models import Student, Faculty, Post
from Main.forms import LoginForm, AddStudents, UpdateAccountForm, PostForm, AddFaculties, RequestResetForm, ResetPasswordForm
from Main import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    # if current_user.is_authenticated:
     #    return redirect(url_for('facultylogin'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id = form.id.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('studenthome'))
        else:
            flash('Login Unsuccessful. Please check id and password', 'danger')
    return render_template('studentlogin.html', title='Login', form=form)

@app.route("/facultylogin", methods=['GET', 'POST'])
def facultylogin():
     #if current_user.is_authenticated:
     #    return redirect(url_for('facultylogin'))
    form = LoginForm()
    if form.validate_on_submit():
        faculty = Faculty.query.filter_by(id = form.id.data).first()
        if faculty and bcrypt.check_password_hash(faculty.password, form.password.data):
            login_user(faculty, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('facultyhome'))
        else:
            flash('Login Unsuccessful. Please check id and password', 'danger')
    return render_template('facultylogin.html', title='Login', form=form)


@app.route('/studenthome')
def studenthome():
    return render_template('studenthome.html')

@app.route('/facultyhome')
def facultyhome():
    return render_template('facultyhome.html')


@app.route('/add/student', methods = ['GET', 'POST'])
def AddStudent():
    form = AddStudents()
    if form.validate_on_submit():
        student = Student(name = form.name.data, id = form.id.data, email = form.email.data, password = bcrypt.generate_password_hash
                                                                                    (form.name.data + str(form.id.data % 100)).decode('utf-8'))
        db.session.add(student)
        db.session.commit()
        flash('Student added!', category="success")
        form.id.data = None
        form.name.data = None
        #next_page = request.args.get('next')
        #return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
        flash('Student couldnt be added', category='success')
    return render_template('adduser.html', form = form)


@app.route('/add/faculty', methods = ['GET', 'POST'])
def AddFaculty():
    form = AddFaculties()
    if form.validate_on_submit():
        faculty = Faculty( id = form.id.data, course = form.course.data, name = form.name.data, email = form.email.data, password = bcrypt.generate_password_hash
                                                                                    (str(form.id.data) ).decode('utf-8'))
        db.session.add(faculty)
        db.session.commit()
        flash('Faculty added!', category="success")
        form.id.data = None
        form.course.data = None
        form.name.data = None
        form.email.data = None
        #next_page = request.args.get('next')
        #return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
        flash('Faculty couldnt be added', category='danger')
    return render_template('addfaculty.html', form = form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
    image_file = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)

@app.route("/new/post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('view_posts'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route('/view/post')
@login_required
def view_posts():
    posts = Post.query.all()
    return render_template('view_posts.html', posts = posts)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_posts.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('facultyhome'))


def send_reset_email(student):
    token = student.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[student.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        send_reset_email(student)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('studentlogin'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    student = Student.verify_reset_token(token)
    if student is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('studentlogin'))
    return render_template('reset_token.html', title='Reset Password', form=form)