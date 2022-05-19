import flask
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import processing as prc
import calls
from user import User


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secret!'# put in config file?


'''
INCOMPLETE
'''
@login_manager.user_loader
def user_loader(email):
    user_obj = calls.get_user_record_email(email)
    if user_obj:
        return User(email)
    else:
        return None


'''
INCOMPLETE
'''
@app.route('/logout')
def logout():
    temp_array = prc.get_orders_top()
    logout_user()
    flask.flash('logged out')
    return render_template('index.html', temp_array=temp_array)


'''
INCOMPLETE
'''
@app.route('/', methods=['post', 'get'])
def index():
    temp_array = prc.get_orders_top()

    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')
        if calls.is_user(email, password):
            user_obj = User(email)
            login_user(user_obj)
            return render_template('account.html')
        else:
            print("failed login")
            return render_template('index.html', temp_array=temp_array)
    else:
        return render_template('index.html', temp_array=temp_array)


'''
INCOMPLETE
'''
@app.route('/account')
@login_required
def account():
    return render_template('account.html')


'''
INCOMPLETE
'''
@app.route('/market')
def market():
    return render_template('market.html')


if __name__ == '__main__':
    app.run(debug=True)
    #print(user_loader("theman@gmail.com"))
