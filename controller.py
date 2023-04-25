from datetime import datetime
import hashlib
import logging
from logging.handlers import RotatingFileHandler
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    session,
    jsonify,
    send_from_directory
)

from service import UserService

logger = logging.getLogger()
logFormatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

fileHandler = logging.FileHandler("applogs.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.WARNING)
consoleHanlder = logging.StreamHandler()
consoleHanlder.setFormatter(logFormatter)

logger.addHandler(consoleHanlder)
logger.addHandler(fileHandler)

app = Flask(__name__)
app.secret_key = '1234'


def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()


@app.route('/')
def index():
    return render_template('signin.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            if (userService.authenticate(str(username), str(password))):
                app.secret_key = generate_key(username)
                data = userService.refreshUser(username)
                response = app.make_response(render_template(
                    'app.html', data=data, len=len(data), username=username))
                session['user_id'] = username
                response.set_cookie('access_time', str(datetime.now()))
                app.logger.warning(f'{username} logged in !')
                return response
            else:
                return render_template('signin.html', error_auth='login or password incorrect')
        except:
            return redirect('/')
    else:
        if ('user_id' in session):
            data = userService.getUserData(session['user_id'])
            return render_template('app.html', data=data, len=len(data), username=session['user_id'])
        return redirect('/')


@app.route('/getdata', methods=["GET"])
def getdata():
    if ('user_id' in session):
        data = userService.refreshUser(session['user_id'])
        return render_template('app.html', data=data, len=len(data), username=session['user_id'])
    return redirect('/')


@app.route('/readfile/<path:path_param>', methods=["GET"])
def readfile(path_param):
    if ('user_id' in session):
        response_data = {
            'status': 'success',
            'data': userService.readFile(f'/{path_param}')
        }
        return jsonify(response_data)
    return redirect('/')


@app.route('/search/<string:search_keyword>', methods=['GET'])
def searchfile(search_keyword):
    if ('user_id' in session):
        response_data = {
            'status': 'success',
            'data': userService.searchFile(session['user_id'], search_keyword)
        }
        return jsonify(response_data)
    return redirect('/')


@app.route('/makearchive', methods=["GET"])
def makearchive():
    if ('user_id' in session):
        directory = '/home'
        filename = f"{session['user_id']}.zip"
        userService.makeArchive(session['user_id'])
        app.logger.warning(f"{session['user_id']} download archive")
        return send_from_directory(directory, filename, as_attachment=True)
    return redirect('/')


@app.route('/logout')
def logout():
    app.logger.warning(f"{session['user_id']} logged out !")
    session.pop('user_id', None)
    return redirect('/')


if (__name__ == "__main__"):
    userService = UserService()
    app.run(host="0.0.0.0", port=9090, debug=True)
