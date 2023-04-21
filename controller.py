from datetime import datetime
import hashlib
from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
)

from service import UserService

app=Flask(__name__)
app.secret_key='1234'

def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template('signin.html') 

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        if (userService.authenticate(str(username), str(password))):
            app.secret_key=generate_key(username)
            data = userService.getUserData(username)
            response=app.make_response(render_template('app.html', data = data))
            session['user_id']=username
            response.set_cookie('access_time',str(datetime.now()))
            return response
        else:
            return render_template('signin.html',error_auth='login or password incorrect')
    else:
        if('user_id' in session):
            data = userService.getUserData(session['user_id'])
            return render_template('app.html', data=data)
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if(__name__ == "__main__"):
    userService = UserService()
    app.run(host="0.0.0.0",port=9090, debug=True)