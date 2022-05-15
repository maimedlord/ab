from flask import Flask, render_template, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_socketio import SocketIO
import processing


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
login_mgr = LoginManager()
socketio = SocketIO(app)

@app.route('/')
def index():
    temp_array = processing.get_orders_top()
    return render_template('index.html', temp_array=temp_array)


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/market')
def market():
    return render_template('market.html')


if __name__ == '__main__':
    socketio.run(app)#app.run(debug=True)
