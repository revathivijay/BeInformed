from Main import db, login_manager, app
from flask_login import  UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_student(id):
    return Student.query.get(int(id))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(35), nullable =False)
    #username = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), default = 'default.jpeg')
    password = db.Column(db.String(60), nullable = False)
    year = db.Column(db.String(20), default = 'x')
    # dob = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # def get_reset_token(self, expires_sec = 1800):\
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'id': self.id}).decode('utf-8')
    #
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         id = s.load(token)['user_id']
    #     except:
    #         return None
    #     return User.query.ger

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.image_file}')"

class Faculty(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
   # username = db.Column(db.String(20), unique = True, nullable =False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), default = 'photo.jpeg')
    password = db.Column(db.String(60), nullable = False)
    course = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"User('{self.id}',  '{self.image_file}', '{self.course}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
