from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
#from flask_socketio import SocketIO
import processing


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
login_mgr = LoginManager()


@app.route('/', methods=['post', 'get'])
def index():
    if "email" in session:
        return redirect(url_for('logged_in'))
    if request.method == 'POST':
        user = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_found = request.form.get('...')
        email_found = request.form.get('.....')
        if user_found:
            message = 'There is already a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists.'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'incorrect password'
            return render_template('index.html', message=message)
        else:
            user_input = {'name': user, 'email': email, 'password': password2}
            #records.insert_one(user_input) # records = database collection
            #user_data = records.find_one({'email': email})
            #new_email = user_data['email']
            #return render_template('logged_in.html', email=new_email)
            pass

    temp_array = processing.get_orders_top()
    return render_template('index.html', temp_array=temp_array)


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/market')
def market():
    return render_template('market.html')


if __name__ == '__main__':
    app.run(debug=True)
