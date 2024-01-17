from flask import Flask, render_template, url_for, request, make_response, redirect

app = Flask(__name__)


@app.route('/')
def index():
    user_name = request.cookies.get('user_name')
    return render_template('index.html', **{'user_name': user_name})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('name') if request.form.get('name') else 'NoName'
        response = make_response(render_template('index.html', **{'user_name': user_name}))
        response.set_cookie('user_name', user_name)
        response.set_cookie('e_mail', request.form.get('email'))
        return response
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    response = make_response(render_template('index.html'))
    response.delete_cookie('user_name')
    response.delete_cookie('e_mail')
    return response


if __name__ == '__main__':
    app.run(debug=True)
