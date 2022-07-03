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


@app.route('/')
def index():
    data_obj = {"ip_address": request.remote_addr}
    c_top = prc.get_contracts_top()
    return render_template('index.html', c_top=c_top, data_obj=data_obj)


@app.route('/accept_offer/<bhunter_id>/<contract_id>/<offer>')
@login_required
def accept_offer(bhunter_id, contract_id, offer):
    result = prc.prc_accept_offer(bhunter_id, contract_id, offer)
    if result:
        return redirect(url_for('contract', contract_id=contract_id, message='none'))
    message = 'there was an error processing your offer acceptance...'
    return redirect(url_for('contract', contract_id=contract_id, message=message))


@app.route('/account')
@login_required
def account():
    data_obj = {"ip_address": request.remote_addr}
    user_orders = prc.process_user_orders(current_user.id_object)
    if user_orders:
        total_earned = 0.0
        for obj in user_orders:
            if obj['bhunter'] == current_user.id_object and obj['phase'] == 'successful':
                total_earned += obj['bounty']
                total_earned += obj['efbonus']
                total_earned += obj['egbonus']
                data_obj['total_earned'] = total_earned
    return render_template('account.html', data_obj=data_obj, user_orders=user_orders)


@app.route('/approve_submission/<contract_id>', methods=['GET', 'POST'])
@login_required
def approve_submission(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['owner'] != current_user.id_object:
            data_obj['message'] = 'you are not authorized to view this contract...'
            return render_template('hmm.html', data_obj=data_obj)
        # ...
        if request.method == 'POST':
            approval = request.form['a_f_approval']
            result = prc.prc_submit_approval(contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
            return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/cancel_contract/<contract_id>')
@login_required
def cancel_contract(contract_id):
    data_obj = {"ip_address": request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj and contract_obj['owner'] != current_user.id_object:
        data_obj['message'] = 'you are not authorized to be here...'
        return render_template('hmm.html', data_obj=data_obj)
    result = calls.cancel_contract(contract_id)
    if result.acknowledged:
        return redirect(url_for('account'))
    data_obj['message'] = 'there was an error canceling the contract'
    return render_template('hmm.html', data_obj=data_obj)



@app.route('/create_contract', methods=['GET', 'POST'])
@login_required
def create_contract():
    data_obj = {"ip_address": request.remote_addr}
    if request.method == 'POST':
        prc_return = prc.process_new_contract(request.form, current_user.id_object)
        if prc_return is None:
            data_obj.update({"message": "processing for your contract failed..."})
            return render_template('create_contract.html', data_obj=data_obj)
        return redirect(url_for('account'))
        # data_obj.update({"message": "you created a contract successfully"})
        # return render_template('success.html', data_obj=data_obj)
    return render_template('create_contract.html', data_obj=data_obj)


@app.route('/contract/<contract_id>/<message>', methods=['GET', 'POST'])
@login_required
def contract(contract_id, message):
    data_obj = {'ip_address': request.remote_addr}
    data_obj.update({'message': message})
    #contract_obj = calls.c_get_contract(contract_id)
    contract_obj = prc.prc_get_contract_account(contract_id, current_user.id_object)
    if not contract_obj:
        data_obj.update({'message': 'contract not found or you are not permitted to view it'})
        return render_template('hmm.html', data_obj=data_obj)
    # PHASE: CREATION
    if contract_obj and contract_obj['phase'] == 'creation' and contract_obj['owner'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # IPARTIES
    iparty_arr = contract_obj['iparties']
    for doc in iparty_arr:
        if doc['bhunter'] == current_user.id_object:
            data_obj.update({'bhunter_offer': doc})
    # PHASE: OPEN
    if contract_obj and contract_obj['phase'] == "open":
        if contract_obj['owner'] != current_user.id_object:
            # form for making an offer:
            if request.method == 'POST':
                offer = float(request.form['m_o_f_offer'])
                result = prc.prc_create_ip(contract_obj['_id'], current_user.id_object, offer)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='none'))
                else:
                    return redirect(url_for('contract', contract_id=contract_id, message='error in process of updating interested parties...'))
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
        else:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # PHASE: INPROGRESS
    if contract_obj and contract_obj['phase'] == 'inprogress' and contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        # form for submitting chat
        if request.method == 'POST':
            message = request.form['c_s_f_message']
            mood = request.form['c_s_f_mood']
            result = prc.prc_send_chat(contract_obj['_id'], current_user.id, message, mood)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
            data_obj['message'] = 'chat send failed!'
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # PHASE: STALLED
    if contract_obj and contract_obj['phase'] == 'stalled':
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: validation
    if contract_obj and contract_obj['phase'] == 'validation' and contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: approved
    if contract_obj and contract_obj['phase'] == 'approved' and contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: gradevalidation
    if contract_obj and contract_obj['phase'] == 'gradevalidation' and contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: rating
    if contract_obj and contract_obj['phase'] == 'rating' and contract_obj[
        'owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: successful
    if contract_obj and contract_obj['phase'] == 'successful' and contract_obj[
        'owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: disputed
    if contract_obj and contract_obj['phase'] == 'disputed':
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # rejected
    data_obj.update({'message': 'contract not found or you are not permitted to view it'})
    return render_template('hmm.html', data_obj=data_obj)


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
            calls.log_userlogin(current_user.id_object)
            # next = flask.request.args.get('next')
            # if not is_safe_url(next):
            #     return flask.abort(400)
            return redirect('account')
            # return render_template('login.html', user_obj=user_obj)
    return render_template('login.html', data_obj=data_obj)


@app.route('/logout')
def logout():
    data_obj = {"ip_address": request.remote_addr}
    if not current_user.is_authenticated:
        data_obj.update({"message": "You're already logged out tho..."})
    calls.log_userlogout(current_user.id_object)
    logout_user()
    return render_template('logout.html', data_obj=data_obj)


@app.route('/market', methods=['post', 'get'])
@login_required
def market():
    data_obj = {"ip_address": request.remote_addr}
    all_open_arr = calls.get_all_open()
    if all_open_arr:
        return render_template('market.html', all_open_arr=all_open_arr, data_obj=data_obj)
    return render_template('market.html', data_obj=data_obj)


@app.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    data_obj = {"ip_address": request.remote_addr}
    if request.method == 'POST':
        email = request.form['r_f_email']
        password1 = request.form['r_f_password1']
        password2 = request.form['r_f_password2']
        username = request.form['r_f_username']
        # where login to test if passwords match?
        result = prc.process_new_user(email, password1, username)
        if result:
            user_arr = calls.get_auth_user(email, password1)
            login_user(User(user_arr[0], user_arr[1], user_arr[2], user_arr[3]))
            # next = flask.request.args.get('next')
            # if not is_safe_url(next):
            #     return flask.abort(400)
            return redirect('account')
    return render_template('register.html', data_obj=data_obj)


# @app.route('/set_disputed/<contract_id>')
# @login_required
# def set_disputed(contract_id):
#     print(contract_id)
#     data_obj = {"ip_address": request.remote_addr}
#     result = prc.prc_set_disputed(contract_id, 'reason')
#     if result:
#         #print(result)
#         return redirect(url_for('contract', contract_id=contract_id))
#     data_obj['message'] = 'setting phase to disputed failed!'
#     return render_template('contract.html', data_obj=data_obj)


@app.route('/set_dors/<contract_id>', methods=['GET', 'POST'])
@login_required
def set_dors(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['bhunter'] != current_user.id_object and contract_obj['owner'] != current_user.id_object:
            data_obj['message'] = 'you are not authorized to view this contract...'
            return render_template('hmm.html', data_obj=data_obj)
        # ...
        if request.method == 'POST':
            dors = request.form['s_f_d_yon']
            if dors == 'disputed':
                result = prc.prc_set_disputed(contract_id, 'disputed: bhunter disputes grade proof')
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='none'))
                return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
            if dors == 'rating':
                result = prc.prc_set_rating(contract_id)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='none'))
                return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
            data_obj['message'] = 'dors didn\'t equal out to either option'
            return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/set_open/<contract_id>')
@login_required
def set_open(contract_id):
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        if contract_obj and contract_obj['owner'] == current_user.id_object:
            result = prc.prc_set_open(contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
    data_obj = {'ip_address': request.remote_addr}
    data_obj['message'] = 'there was an error setting the contract to open'
    return render_template('hmm.html', data_obj=data_obj)


@app.route('/set_successful/<contract_id>', methods=['GET', 'POST'])
@login_required
def set_successful(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    pass


@app.route('/submit_assignment/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['bhunter'] != current_user.id_object:
            data_obj['message'] = 'you are not authorized to view this contract...'
            return render_template('hmm.html', data_obj=data_obj)
        # ...
        if request.method == 'POST':
            submission = request.form['s_f_submission']
            result = prc.prc_submit_assignment(contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
            return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/submit_grade/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_grade(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['owner'] != current_user.id_object:
            data_obj['message'] = 'you are not authorized to view this contract...'
            return render_template('hmm.html', data_obj=data_obj)
        # ...
        if request.method == 'POST':
            grade = request.form['s_f_grade']
            grade_proof = request.form['s_f_yon']
            result = prc.prc_submit_gvalidation(contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
            return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/submit_rating/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_rating(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['bhunter'] == current_user.id_object or contract_obj['owner'] == current_user.id_object:
            if request.method == 'POST':
                user_id = current_user.id_object
                comment = request.form['s_r_f_comment']
                rating = request.form['s_r_f_rating']
                result = prc.prc_submit_rating_c(comment, contract_id, rating, user_id)
                if result:
                    print('form worked')
                    return redirect(url_for('contract', contract_id=contract_id, message='none'))
            # form didn't work...
            return redirect(url_for('contract', contract_id=contract_id, message='none'))
        data_obj['message'] = 'you are not authorized to view this contract...'
        return render_template('hmm.html', data_obj=data_obj)
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/success')
@login_required
def success():
    data_obj = {"ip_address": request.remote_addr}
    return render_template('success.html', data_obj=data_obj)


@app.route('/validate_submission/<contract_id>', methods=['GET', 'POST'])
@login_required
def validate_submission(contract_id):
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        pass
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/view_user/<userid>')
@login_required
def view_user(userid):
    data_obj = {"ip_address": request.remote_addr}
    user_obj = calls.get_user(userid)
    if user_obj:
        user_obj = dict(user_obj)
        print(user_obj)
        return render_template('view_user.html', data_obj=data_obj, user_obj=user_obj)
    data_obj['message'] = "no user found..."
    return render_template('view_user.html', data_obj=data_obj)


if __name__ == '__main__':
    print(register())
    app.run(debug=True)
    # print(user_loader("theman@gmail.com"))
