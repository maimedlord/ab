import calls
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from user import User


'''
INCOMPLETE
'''


def accept_offer(contract_id, bhunter_id):
    print(contract_id, bhunter_id)
    # update phase, bhunter
    calls.update_inprogress(ObjectId(contract_id), ObjectId(bhunter_id))
    pass


'''
INCOMPLETE
'''
def get_contracts_top():
    contracts_data = calls.get_contracts_top_10()
    if contracts_data:
        contracts_data = list(contracts_data)
    return contracts_data


'''
INCOMPLETE
WHERE IS THIS?
'''
def get_user_record(email, password):
    user_record = calls.get_user_record(email, password)
    if user_record == {"error": "no record found"}:
        return {}
    else:
        return user_record


'''
INCOMPLETE
'''


def prc_create_ip(contract_id, bhunter_user_id, offer):
    ip_object = {
        'bhunter': bhunter_user_id,
        'offer': offer,
        'time': datetime.fromisoformat(datetime.now().isoformat()[:-7])
    }
    return calls.create_ip(contract_id, ip_object)


'''
INCOMPLETE: 
NEED TO VERIFY ALL INPUT HERE BEFORE SENDING TO CALLS
good return = array of validated form data
'''
def process_new_contract(form_dict, userid):
    # handle a malformed dictionary...
    user_obj = {}
    bounty = float(form_dict['c_f_bounty'])
    user_obj.update({"bounty": bounty})
    user_obj.update({"bhunter": ObjectId("000000000000000000000000")})
    e_f_bonus = float(form_dict['c_f_efbonus'])
    user_obj.update({"efbonus": float(e_f_bonus)})
    e_g_bonus = float(form_dict['c_f_egbonus'])
    user_obj.update({"egbonus": float(e_g_bonus)})
    g_deadline = form_dict['c_f_t_g_deadline']
    if g_deadline != "":
        g_deadline = datetime.fromisoformat(form_dict['c_f_t_g_deadline'] + 'T' + form_dict['c_f_t_g_d_time'] + ':00.000000')
    lostudy = form_dict['c_f_lostudy']
    user_obj.update({"lostudy": lostudy})
    sample = form_dict['c_f_sample']
    user_obj.update({"sample": sample})
    specialization = form_dict['c_f_specialization']
    user_obj.update({"specialization": specialization})
    stall_iso = datetime.fromisoformat(form_dict['c_f_t_stall'] + 'T' + form_dict['c_f_t_s_time'] + ':00')
    start_iso = datetime.fromisoformat(datetime.now().isoformat()[:-7])
    user_obj.update({"clog": []})
    subject = form_dict['c_f_subject']
    user_obj.update({"subject": subject})
    type_contract = form_dict['c_f_type']
    user_obj.update({"type_contract": type_contract})
    # set up assignment contract:
    if type_contract == 'assignment':
        a_deadline_iso = datetime.fromisoformat(form_dict['c_f_t_a_deadline'] + 'T' + form_dict['c_f_t_a_d_time'] + ':00')
        if e_f_bonus != 0.0:
            efbonus_deadline = datetime.fromisoformat(form_dict['c_f_efb_deadline'] + 'T' + form_dict['c_f_efb_d_time'] + ':00')
            user_obj.update({"timeline": [{"time": start_iso, "event": "created"},
                                          {"time": stall_iso, "event": "deadline: stall"},
                                          {"time": a_deadline_iso, "event": "deadline: submission"},
                                          {"time": g_deadline, "event": "deadline: grading"},
                                          {"time": g_deadline, "event": "deadline: rate the other person"},
                                          {"time": efbonus_deadline, "event": "deadline: early finish bonus!"}]})  # MISSING CORRECT RATING DEADLINE
        else:
            user_obj.update({"timeline": [{"time": start_iso, "event": "created"},
                                      {"time": stall_iso, "event": "deadline: stall"},
                                      {"time": a_deadline_iso, "event": "deadline: submission"},
                                      {"time": g_deadline, "event": "deadline: grading"},
                                      {"time": g_deadline, "event": "deadline: rate the other person"}]})# MISSING CORRECT RATING DEADLINE
    # set up assignment contract:
    if type_contract == 'test':
        t_start_iso = datetime.fromisoformat(form_dict['c_f_t_t_start'] + 'T' + form_dict['c_f_t_t_s_time'] + ':00')
        t_end_iso = datetime.fromisoformat(form_dict['c_f_t_t_end'] + 'T' + form_dict['c_f_t_t_e_time'] + ':00')
        user_obj.update({"timeline": [{"time": start_iso, "event": "created"},
                                      {"time": stall_iso, "event": "deadline: stall"},
                                      {"time": t_start_iso, "event": "deadline: test start"},
                                      {"time": t_end_iso, "event": "deadline: test end"},
                                      {"time": g_deadline, "event": "deadline: grading"},
                                      {"time": g_deadline, "event": "deadline: rate the other person"}]})# MISSING CORRECT RATING DEADLINE
    # add in data not initiated by user:
    user_obj.update({"owner": userid})
    user_obj.update({"iparties": []})
    user_obj.update({"clog": [{"time": start_iso, "event": "created"}]})
    user_obj.update({"phase": "creation"})
    user_obj.update({'reviews': []})
    result = calls.create_contract(user_obj)
    return result


'''
INCOMPLETE
'''


def process_new_user(email, password1, username):
    user_template = {
        'active': True,
        'email': email,
        'pass': generate_password_hash(password1),
        'uName': username,
        'joinDate': datetime.fromisoformat(datetime.now().isoformat()[:-7]),
        'timezone': 'sometimezonezzz',
        'reviewHistory': []
    }
    return calls.create_user(user_template)


    #     if result:
    #         user_obj = User(email, username)
    #         login_user(user_obj)
    #         # next = flask.request.args.get('next')
    #         # if not is_safe_url(next):
    #         #     return flask.abort(400)
    #         return render_template('success.html')
    #     else:
    #         data_obj.update({"message": "email or username is already taken. try again"})
    #         return render_template('register.html', data_obj=data_obj)
    pass


'''
INCOMPLETE
'''


def process_user_orders(userid_obj):
    cursor_obj = calls.get_user_contracts(userid_obj)
    if cursor_obj:
        obj_arr = []
        for doc in cursor_obj:
            obj_arr.append(doc)
            print(obj_arr[-1]['timeline'][3]['time'])
        return obj_arr
    else:
        return None


if __name__ == '__main__':
    print(get_user_record('theman@gmail.com', 'passwordpass'))