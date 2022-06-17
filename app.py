from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, request, session, url_for, flash, Markup
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import processing as prc
import calls
# import html
from user import User
from forms import CContract, LoginForm, RegistrationForm


# NEXT AFTER LOGIN_USER - SEE FLASK-LOGIN DOCUMENTATION


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secret!'  # put in config file?


'''
...
'''


@login_manager.user_loader
def user_loader(user_id):
    user_arr = calls.get_sesh(user_id)
    if len(user_arr) > 0:
        return User(user_arr[0], user_arr[1], user_arr[2], user_arr[3])
    else:
        return None


'''
INCOMPLETE
'''


@app.route('/')
def index():
    data_obj = {"ip_address": request.remote_addr}
    return render_template('index.html', data_obj=data_obj)


'''
INCOMPLETE
'''


@app.route('/account')
@login_required
def account():
    data_obj = {"ip_address": request.remote_addr}
    data_obj.update({"ip_address": request.remote_addr})
    user_orders = calls.get_user_orders(current_user.id_object)
    return render_template('account.html', data_obj=data_obj, user_orders=user_orders)


'''
INCOMPLETE
'''


@app.route('/create_contract', methods=['post', 'get'])
@login_required
def create_contract():
    data_obj = {"ip_address": request.remote_addr}
    if request.method == 'POST':
        prc_return = prc.process_new_contract(request.form, current_user.id_object)
        if prc_return is None:
            data_obj.update({"message": "processing for your contract failed..."})
            return render_template('create_contract.html', data_obj=data_obj)
        data_obj.update({"message": "you created a contract successfully"})
        return render_template('success.html', data_obj=data_obj)
    return render_template('create_contract.html', data_obj=data_obj)


'''
INCOMPLETE
'''


@app.route('/login', methods=['post', 'get'])
def login():
    data_obj = {"ip_address": request.remote_addr}
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_arr = calls.get_auth_user(email, password)
        # userid = str(user_obj['_id'])
        if user_arr:
            # for doc in user_arr:
            #     print(doc)
            #print(user_arr)
            login_user(User(user_arr[0], user_arr[1], user_arr[2], user_arr[3]))
            # next = flask.request.args.get('next')
            # if not is_safe_url(next):
            #     return flask.abort(400)
            return redirect('account')
            # return render_template('login.html', user_obj=user_obj)
    return render_template('login.html', data_obj=data_obj)


'''
INCOMPLETE
'''


@app.route('/logout')
def logout():
    data_obj = {"ip_address": request.remote_addr}
    if not current_user.is_authenticated:
        data_obj.update({"message": "You're already logged out tho..."})
    logout_user()
    return render_template('logout.html', data_obj=data_obj)


'''
INCOMPLETE
'''


@app.route('/market', methods=['post', 'get'])
@login_required
def market():
    data_obj = {"ip_address": request.remote_addr}
    return render_template('market.html', data_obj=data_obj)


'''
INCOMPLETE
'''


@app.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    data_obj = {"ip_address": request.remote_addr}
    temp_array = prc.get_orders_top()
    if request.method == 'POST':
        email = request.form.get('user_email')
        password1 = request.form.get('user_password1')
        password2 = request.form.get('user_password2')
        username = request.form.get('username')
        if email == '' or password1 == '' or password2 == '' or username == '':
            return render_template('register.html', passed=data_obj, temp_array=temp_array)
        dict_template = {
            'active': True,
            'email': email,
            'pass': generate_password_hash(password1),
            'uName': username,
            'joinDate': 'some date for sure 2',
            'orders': []
        }
        result = calls.create_user(dict_template)
        if result:
            user_obj = User(email, username)
            login_user(user_obj)
            # next = flask.request.args.get('next')
            # if not is_safe_url(next):
            #     return flask.abort(400)
            return render_template('success.html')
        else:
            data_obj.update({"message": "email or username is already taken. try again"})
            return render_template('register.html', data_obj=data_obj)

    return render_template('register.html', data_obj=data_obj, temp_array=temp_array)


'''
INCOMPLETE
'''


@app.route('/success')
@login_required
def success():
    data_obj = {"ip_address": request.remote_addr}
    return render_template('success.html', data_obj=data_obj)


# '''
# INCOMPLETE
# '''
# @login_manager.unauthorized_handler
# def unauthorized():
#     temp_array = prc.get_orders_top()
#     return render_template('index.html', temp_array=temp_array)


if __name__ == '__main__':
    print(register())
    app.run(debug=True)
    # print(user_loader("theman@gmail.com"))
