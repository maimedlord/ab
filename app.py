import os
from flask import Flask, redirect, render_template, request, session, url_for, flash, Markup, send_from_directory, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from jinja2 import Environment
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, urljoin
import processing as prc
import calls
import contextlib
import re
from datetime import datetime  # get this moved to prc...
# import html
from user import User
from forms import CContract, LoginForm, RegistrationForm


app = Flask(__name__)


# NEED to verify safe next as used in login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = 'you need to be logged in and authorized to view this page...'
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'secret!'  # put in config file?
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'gif', 'jpg', 'pdf', 'png', 'txt'}
NO_CHAT_MSG_ARR = ['creation', 'open', 'successful']


# for uploading files...
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# for logging in user... // MIGHT NEED TO GET PRESENT FOR ALL REDIRECTS???
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# for removing dangerous characters from strings passed to routes via POST/address
def remove_danger_chars(passed_string):
    return re.sub("[$;:&@?*%<>{}|,\[\]^]", '', passed_string)


@login_manager.user_loader
def user_loader(user_id):
    user_arr = calls.get_sesh(user_id)
    if len(user_arr) > 0:
        return User(user_arr[0], user_arr[1], user_arr[2], user_arr[3], user_arr[4])
    else:
        return None


#######################################################################################################################


@app.route('/')
def index():
    data_obj = {"ip_address": request.remote_addr}
    c_top = prc.get_contracts_top()
    return render_template('index.html', c_top=c_top, data_obj=data_obj)


@app.route('/accept_ip_offer/<bhunter_id>/<bhunter_uname>/<contract_id>/<offer>')
@login_required
def accept_ip_offer(bhunter_id, bhunter_uname, contract_id, offer):
    bhunter_id = remove_danger_chars(bhunter_id)
    contract_id = remove_danger_chars(contract_id)
    offer = remove_danger_chars(offer)
    # authorization:
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj['owner'] != current_user.id_object:
        return redirect(url_for('hmm', message='you are not authorized to view this contract...'))
    result = prc.prc_accept_offer(bhunter_id, bhunter_uname, contract_id, offer)
    if result:
        return redirect(url_for('contract', contract_id=contract_id, message='none'))
    message = 'there was an error processing your offer acceptance...'
    return redirect(url_for('contract', contract_id=contract_id, message=message))


@app.route('/account')
@login_required
def account():
    data_obj = {"ip_address": request.remote_addr, 'new_msg_arr': None, 'no_chat_msg_arr': NO_CHAT_MSG_ARR}
    user_contracts_obj = prc.process_user_orders(current_user.id_object)
    user_obj = prc.get_user_record(current_user.id_object)
    # average rating:
    if user_obj:
        user_obj = dict(user_obj)
        if len(user_obj['reviewHistory']) > 0:
            data_obj['review_avg'] = 0.0
            counter = 0
            for x in user_obj['reviewHistory']:
                data_obj['review_avg'] += x['rating']
                counter += 1
            data_obj['review_avg'] = data_obj['review_avg'] / counter
    # total earned, msg_arr:
    msg_arr = []
    if user_contracts_obj:
        total_earned = 0.0
        for obj in user_contracts_obj:
            # msg_arr:
            if obj['bhunter'] == current_user.id_object and obj['chatnewmsgbhunter']:
                msg_arr.append(str(obj['_id']))
            elif obj['owner'] == current_user.id_object and obj['chatnewmsgowner']:
                msg_arr.append(str(obj['_id']))
            # total earned:
            if obj['bhunter'] == current_user.id_object and obj['phase'] == 'successful':
                total_earned += obj['bounty']
                total_earned += obj['efbonus']
                total_earned += obj['egbonus']
                data_obj['total_earned'] = total_earned
    return render_template('account.html', data_obj=data_obj, msg_arr=msg_arr, user_contracts=user_contracts_obj)


@app.route('/yon_asubmission/<contract_id>', methods=['GET', 'POST'])
@login_required
def yon_asubmission(contract_id):
    contract_id = remove_danger_chars(contract_id)
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['owner'] != current_user.id_object:
            return redirect(url_for('hmm', message='you are not authorized to view this contract...'))
        if request.method == 'POST':
            result = prc.prc_yon_asubmission(request.form, contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='success'))
            return redirect(url_for('contract', contract_id=contract_id,
                                    message='error: processing your submission'))
    return redirect(url_for('contract', contract_id=contract_id, message='error: unable to look up contract...'))


@app.route('/cancel_contract/<contract_id>')
@login_required
def cancel_contract(contract_id):
    contract_id = remove_danger_chars(contract_id)
    data_obj = {"ip_address": request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj and contract_obj['phase'] != 'creation' and contract_obj['owner'] != current_user.id_object:
        data_obj['message'] = 'you are not authorized to be here...'
        return render_template('hmm.html', data_obj=data_obj)
    if contract_obj['sampleUp'] is not None:
        # suppressing FileNotFoundError:
        with contextlib.suppress(FileNotFoundError):
            # remove from local storage:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], contract_obj['sampleUp']))
    # remove contract from db:
    result = calls.cancel_contract(contract_id)
    if result.acknowledged:
        return redirect(url_for('account'))
    data_obj['message'] = 'there was an error canceling the contract'
    return render_template('hmm.html', data_obj=data_obj)


# disable back button?
@app.route('/create_contract', methods=['GET', 'POST'])
@login_required
def create_contract():
    data_obj = {"ip_address": request.remote_addr}
    if request.method == 'POST':
        the_file = request.files['sample_file']
        if the_file and the_file.filename != '' and allowed_file(the_file.filename):
            # process new contract first in db before saving:
            prc_return = prc.process_new_contract(request.form, current_user.id_object, current_user.username, current_user.tz_offset)
            if prc_return.acknowledged:
                filename = secure_filename(the_file.filename)
                filename = str(prc_return.inserted_id) + '-sample-' + filename
                # save uploaded file:
                the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # update db with filename of uploaded file:
                result = calls.c_set_sampleUp(prc_return.inserted_id, filename)
                if result.acknowledged is False:
                    # write to error log
                    data_obj.update({'message': 'processing for your contract failed...'})
                    return render_template('create_contract.html', data_obj=data_obj)
        else:
            prc_return = prc.process_new_contract(request.form, current_user.id_object, current_user.username, current_user.tz_offset)
            if prc_return.acknowledged is False:
                # write to error log
                data_obj.update({'message': 'processing for your contract failed...'})
                return render_template('create_contract.html', data_obj=data_obj)
        # successful:
        return redirect(url_for('account'))
    # initial view:
    return render_template('create_contract.html', data_obj=data_obj)


@app.route('/contract/<contract_id>/<message>', methods=['GET', 'POST'])
@login_required
def contract(contract_id, message):
    contract_id = remove_danger_chars(contract_id)
    message = remove_danger_chars(message)
    data_obj = {'ip_address': request.remote_addr, 'message': message, 'dispute_arr': [
        'inprogress', 'validation', 'approved', 'gvalidation'
    ]}
    contract_obj = prc.prc_get_contract_account(contract_id, current_user.id_object)
    if not contract_obj:
        return redirect(url_for('hmm', message='contract not found or you are not permitted to view it...'))
    # creates potential earnings value:
    data_obj['earnable'] = contract_obj['bounty']
    if contract_obj['efbonusyon']:
        data_obj['earnable'] += contract_obj['efbonus']
    if contract_obj['egbonusyon']:
        data_obj['earnable'] += contract_obj['egbonus']
    # PHASE: CREATION
    if contract_obj and contract_obj['phase'] == 'creation':
        if contract_obj['owner'] == current_user.id_object:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # looks for existing offer in iparties and if exists, passes to data_obj
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
                result = prc.prc_create_ip(contract_obj['_id'], current_user.id_object, current_user.username, offer)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='offer success'))
                return redirect(url_for('contract', contract_id=contract_id, message='error in process of updating interested parties...'))
            # default view for non-owner:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
        # owner view:
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # PHASE: INPROGRESS
    if contract_obj and contract_obj['phase'] == 'inprogress':
        if contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
            print(contract_obj['phase'])
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # PHASE: STALLED
    if contract_obj and contract_obj['phase'] == 'stalled':
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: validation
    if contract_obj and contract_obj['phase'] == 'validation':
        if contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: approved
    if contract_obj and contract_obj['phase'] == 'approved':
        if contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: gradevalidation
    if contract_obj and contract_obj['phase'] == 'gradevalidation':
        if contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: rating
    if contract_obj and contract_obj['phase'] == 'rating':
        if len(contract_obj['reviews']) > 0:
            data_obj['reviewers'] = []
            for review in contract_obj['reviews']:
                data_obj['reviewers'].append(review['user'])

            print(data_obj['reviewers'])
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
        # return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: successful
    if contract_obj and contract_obj['phase'] == 'successful':
        if contract_obj['owner'] == current_user.id_object or contract_obj['bhunter'] == current_user.id_object:
            return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # phase: disputed
    if contract_obj and contract_obj['phase'] == 'disputed':
        return render_template('contract.html', contract_obj=contract_obj, data_obj=data_obj)
    # rejected
    return redirect(url_for('hmm', message='contract not found or you are not permitted to view it...'))


@app.route('/download_grade_proof/<filename>')
@login_required
def download_grade_proof(filename):
    filename = remove_danger_chars(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='/', filename=filename)


@app.route('/download_sample/<filename>')
@login_required
def download_sample(filename):
    filename = remove_danger_chars(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='/', filename=filename)


@app.route('/download_submission/<filename>')
@login_required
def download_submission(filename):
    filename = remove_danger_chars(filename)
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='/', filename=filename)


@app.route('/hmm/<message>')
def hmm(message):
    message = remove_danger_chars(message)
    data_obj = {"ip_address": request.remote_addr, 'message': message}
    return render_template('hmm.html', data_obj=data_obj)


@app.route('/login', methods=['post', 'get'])
def login():
    data_obj = {"ip_address": request.remote_addr}
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tz_offset = request.form['tz_offset']
        user_arr = calls.get_auth_user(email, password, tz_offset)
        if user_arr:
            login_user(User(user_arr[0], user_arr[1], user_arr[2], user_arr[3], user_arr[4]))
            # tracking:
            calls.log_userlogin(current_user.id_object)
            next = request.args.get('next')
            print('YOU NEED TO MAKE SURE THAT THIS LOGIN PROCEDURE IS SAFE: NEXT IS_SAFE_URL(NEXT)')
            print(next)
            if not is_safe_url(next):
                return abort(400)
            return redirect(url_for('account'))
        data_obj['message'] = 'that account does not exist...'
    return render_template('login.html', data_obj=data_obj)


@app.route('/logout')
def logout():
    data_obj = {"ip_address": request.remote_addr}
    if current_user.is_authenticated:
        calls.log_userlogout(current_user.id_object)
        logout_user()
    else:
        data_obj.update({"message": "You're already logged out tho..."})
    return render_template('logout.html', data_obj=data_obj)


@app.route('/market', methods=['get'])
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
        tz_offset = request.form['r_f_timezone']
        username = request.form['r_f_username']
        # where login to test if passwords match?
        result = prc.process_new_user(email, password1, tz_offset, username)
        if result:
            user_arr = calls.get_auth_user(email, password1, tz_offset)
            login_user(User(user_arr[0], user_arr[1], user_arr[2], user_arr[3], user_arr[4]))
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
    contract_id = remove_danger_chars(contract_id)
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
    contract_id = remove_danger_chars(contract_id)
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        if contract_obj and contract_obj['owner'] == current_user.id_object:
            result = prc.prc_set_open(contract_id)
            if result:
                return redirect(url_for('contract', contract_id=contract_id, message='none'))
    data_obj = {'ip_address': request.remote_addr, 'message': 'there was an error setting the contract to open'}
    return render_template('hmm.html', data_obj=data_obj)


@app.route('/set_successful/<contract_id>', methods=['GET', 'POST'])
@login_required
def set_successful(contract_id):
    contract_id = remove_danger_chars(contract_id)
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    pass


@app.route('/submit_assignment/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(contract_id):
    contract_id = remove_danger_chars(contract_id)
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['bhunter'] != current_user.id_object:
            return redirect(url_for('hmm'), message='you are not authorized to view this contract...')
        if request.method == 'POST':
            the_file = request.files['assignment_file']
            if the_file and the_file.filename != '' and allowed_file(the_file.filename):
                filename = secure_filename(the_file.filename)
                filename = contract_id + '-asubmit-' + filename
                the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = prc.prc_submit_assignment(contract_id, filename)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id,
                                            message='assignment successfully submitted...'))
                return redirect(url_for('contract', contract_id=contract_id,
                                        message='there was an error submitting the assignment...'))
            return redirect(url_for('contract', contract_id=contract_id,
                                    message='there was an error processing the uploaded file...'))
    return redirect(url_for('contract', contract_id=contract_id,
                            message='there was an error finding the contract...'))


# NEED TO FIX MAJOR
@app.route('/submit_grade/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_grade(contract_id):
    contract_id = remove_danger_chars(contract_id)
    data_obj = {'ip_address': request.remote_addr}
    contract_obj = calls.c_get_contract(contract_id)
    if contract_obj:
        #  authorization...
        if contract_obj['owner'] != current_user.id_object:
            data_obj['message'] = 'you are not authorized to view this contract...'
            return render_template('hmm.html', data_obj=data_obj)
        # ...
        if request.method == 'POST':
            the_file = request.files['grade_file']
            yon = request.form['s_f_yon']
            if yon == 'true':
                result = prc.prc_submit_gvalidation(contract_id, None)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='success'))
                return redirect(url_for('contract', contract_id=contract_id, message='error: submission process has failed...'))
            if yon == 'false' and the_file and the_file.filename != '' and allowed_file(the_file.filename):
                filename = secure_filename(the_file.filename)
                filename = contract_id + '-grade-' + filename
                the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = prc.prc_submit_gvalidation(contract_id, filename)
                if result:
                    return redirect(url_for('contract', contract_id=contract_id, message='success'))
                return redirect(url_for('contract', contract_id=contract_id, message='error: submission process has failed...'))
    data_obj['message'] = 'the contract was not found'
    return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/submit_rating/<contract_id>', methods=['GET', 'POST'])
@login_required
def submit_rating(contract_id):
    contract_id = remove_danger_chars(contract_id)
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
                    return redirect(url_for('contract', contract_id=contract_id, message='success'))
            # form didn't work...
            return redirect(url_for('contract', contract_id=contract_id,
                                    message='error: something went wrong during submission...'))
        data_obj['message'] = 'you are not authorized to view this contract...'
        return render_template('hmm.html', data_obj=data_obj)
    return redirect(url_for('contract', contract_id=contract_id, message='error: the contract could not be found...'))


@app.route('/success')
@login_required
def success():
    data_obj = {"ip_address": request.remote_addr}
    return render_template('success.html', data_obj=data_obj)


# appears to have been deprecated in favor of approve_submission()
# @app.route('/validate_asubmission/<contract_id>', methods=['GET', 'POST'])
# @login_required
# def validate_asubmission(contract_id):
#     data_obj = {'ip_address': request.remote_addr}
#     contract_obj = calls.c_get_contract(contract_id)
#     if contract_obj:
#         pass
#     data_obj['message'] = 'the contract was not found'
#     return redirect(url_for('contract', contract_id=contract_id, message='none'))  # need to fix this


@app.route('/view_user/<user_id>')
@login_required
def view_user(user_id):
    user_id = remove_danger_chars(user_id)
    data_obj = {"ip_address": request.remote_addr, 'review_avg': None}
    user_obj = calls.get_user(user_id)
    if user_obj:
        user_obj = dict(user_obj)
        # average rating:
        if len(user_obj['reviewHistory']) > 0:
            data_obj['given_avg'] = 0.0
            data_obj['received_avg'] = 0.0
            data_obj['review_avg'] = 0.0
        counter = 0
        for x in user_obj['reviewHistory']:
            data_obj['review_avg'] += x['rating']
            if str(x['reviewer']) == user_id:
                data_obj['given_avg'] += x['rating']
            else:
                data_obj['received_avg'] += x['rating']
            counter += 1
        if data_obj['review_avg'] != None:
            data_obj['given_avg'] = data_obj['given_avg'] / counter
            data_obj['received_avg'] = data_obj['received_avg'] / counter
            data_obj['review_avg'] = data_obj['review_avg'] / counter
        else:
            data_obj['review_avg'] = 'no reviews yet'
        return render_template('view_user.html', data_obj=data_obj, user_obj=user_obj)
    data_obj['message'] = "no user found..."
    return render_template('view_user.html', data_obj=data_obj)


if __name__ == '__main__':
    print(register())
    app.run(debug=True)
    # print(user_loader("theman@gmail.com"))
