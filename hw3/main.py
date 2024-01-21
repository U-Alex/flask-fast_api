from flask import Flask, render_template, url_for, request, make_response, redirect, flash
from flask_wtf.csrf import CSRFProtect
from hashlib import sha3_384

from model import db, User
from form import RegForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'79dd818845851fb984160b95113596c5bd27cf49f26a944f0b42f7c2c83cbf70'
# app.secret_key = b'79dd818845851fb984160b95113596c5bd27cf49f26a944f0b42f7c2c83cbf70'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    context = {'user_name': request.cookies.get('user_name')}
    if not context.get('user_name'):
        context['form'] = LoginForm()
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.login == form.login.data).first()
        if not user:
            flash('login not found')
            return redirect(url_for('login'))
        if user.password != get_hex_digest(form.password.data):
            flash('password not valid')
            return redirect(url_for('login'))
        user_name = f"{user.firstname} {user.lastname}"
        response = make_response(render_template('index.html', **{'user_name': user_name}))
        response.set_cookie('user_name', user_name)
        return response

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    response = make_response(render_template('index.html', **{'form': LoginForm()}))
    response.delete_cookie('user_name')
    return response


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    if request.method == 'POST' and form.validate():
        user = User(login=form.login.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=get_hex_digest(form.password.data)
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('registration.html', form=form)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('ok')


def get_hex_digest(password):
    return sha3_384(password.encode('utf-8')).hexdigest()



