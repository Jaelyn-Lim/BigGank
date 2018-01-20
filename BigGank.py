from flask import Flask, render_template, redirect, request, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager, current_user, login_user, login_required, login_fresh, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
manager = Manager(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u'请登录'
login_manager.session_protection = 'strong'
login_manager.init_app(app)


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    user = Users.query.filter_by(id=id).first()
    return user

@app.route('/delete')
def delete():
    text_type = request.args.get('id')
    print(text_type)
    infos = Info.query.filter_by(id=int(text_type)).first()
    print(infos.id)
    db.session.delete(infos)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
def index(text_type='all'):
    TEXT_TYPE = {
        'all': u'首页',
        'ios': 'IOS',
        'android': 'Android',
        'qianduan': u'前端',
        'tuozhang': u'拓展资源',
    }
    text_type = request.args.get('typy')
    if text_type is None or text_type == 'all':
        infos = Info.query.all()
        text_type = 'all'
    else:
        infos = Info.query.filter_by(typy=TEXT_TYPE.get(text_type)).all()
    return render_template('index.html', user=current_user, texttype=TEXT_TYPE.get(text_type),
                           infos=infos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        login_fresh()
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # user = db.session.query(Users).filter(Users.email == form.email.data).first()
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber.data)
            flash('登录成功.')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('邮箱或密码错误')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data,
                     username=form.username.data,
                     password_hash=generate_password_hash(form.password.data))
        user.save()
        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('register.html', form=form)


@app.route('/usercenter', methods=['GET', 'POST'])
def usercenter():
    return render_template('usercenter.html')


@app.route('/useredit', methods=['GET', 'POST'])
def useredit():
    form = EditForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=g.user.email).first()
        print(form.password.data)
        user.password_hash = generate_password_hash(form.password.data)
        user.save()
        return redirect(request.args.get('next') or url_for('usercenter'))
    return render_template('useredit.html', form=form)


class EditForm(FlaskForm):
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码必填！')])
    password2 = PasswordField(u'确认密码',
                              validators=[DataRequired(message=u'密码必填！'), EqualTo('password', message=u'密码不匹配')])
    submit = SubmitField(u'修改')


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remeber = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(message=u'邮箱必填！'), Length(1, 64), Email(message=u'邮箱格式不正确！')])
    username = StringField(u'用户名',
                           validators=[DataRequired(message=u'用户名必填！'), Length(1, 64),
                                       Regexp('^[A-Za-z0-9][A-Za-z0-9]*$', 0,
                                              message='用户名只能有字母数字组成')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码必填！')])
    password2 = PasswordField(u'确认密码',
                              validators=[DataRequired(message=u'密码必填！'), EqualTo('password', message=u'密码不匹配')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            print(u'邮箱已存在')
            raise ValidationError(u'邮箱已存在')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            print(u'用户名已存在')
            raise ValidationError(u'用户名已存在')


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash

    @property
    def password(self):
        raise AttributeError(u'密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(64))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    desc = db.Column(db.String(128), unique=True, index=True)
    publishedAt = db.Column(db.DateTime(), default=datetime.utcnow)
    source = db.Column(db.String(32))
    typy = db.Column(db.String(32))
    url = db.Column(db.String(64))
    used = db.Column(db.Boolean, default=False)
    who = db.Column(db.String(64))


if __name__ == '__main__':
    # manager.run()
    app.run()
