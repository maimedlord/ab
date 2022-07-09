import calls
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from user import User

def get_contracts_top():
    contracts_data = calls.get_contracts_top_10()
    if contracts_data:
        contracts_data = list(contracts_data)
    return contracts_data


def get_user_record(email, password):
    user_record = calls.get_user_record(email, password)
    if user_record == {"error": "no record found"}:
        return {}
    else:
        return user_record


def prc_accept_offer(bhunter_id, contract_id, bhunter_offer):
    clog_obj = {
        'event': 'bounty hunter offer accepted and phase set to inprogress',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    }
    result = calls.c_accept_offer(ObjectId(contract_id), ObjectId(bhunter_id), float(bhunter_offer), clog_obj)
    if result.acknowledged:
        return True
    return None


def prc_get_contract_account(contract_id, user_id):
    nowtime = datetime.fromisoformat(datetime.now().isoformat())
    result = calls.c_get_contract(ObjectId(contract_id))
    if result:
        if result['bhunter'] == ObjectId(user_id):
            return calls.c_getset_lvbhunter(ObjectId(contract_id), datetime.fromisoformat(datetime.now().isoformat()))
        if result['owner'] == ObjectId(user_id):
            return calls.c_getset_lvowner(ObjectId(contract_id), datetime.fromisoformat(datetime.now().isoformat()))
    return result



def prc_create_ip(contract_id, bhunter_user_id, offer):
    ip_object = {
        'bhunter': bhunter_user_id,
        'offer': offer,
        'time': datetime.fromisoformat(datetime.now().isoformat())
    }
    return calls.c_create_ip(contract_id, ip_object)


def prc_send_chat(contractid, userid, message, mood):
    nowtime = datetime.fromisoformat(datetime.now().isoformat())
    result = calls.c_send_chat(ObjectId(contractid), {'message': message, 'mood': mood, 'time': nowtime, 'user': ObjectId(userid)})
    if result:
        if result.acknowledged:
            return True
    return None


def prc_set_disputed(contract_id, reason):
    # need to also update changelog and message to both users...
    # what phase is contract in when set to dispute?
    # alert admin to look at contract and make a finding/judgement.
    # return calls.c_set_disputed(ObjectId(contract_id))
    result = calls.c_set_disputed(ObjectId(contract_id), {
        'event': reason,
        'time': datetime.fromisoformat(datetime.now().isoformat())
    })
    if result.acknowledged:
        #  stuff to do...???
        return True
    return None


def prc_set_rating(contract_id):
    result = calls.c_set_rating(ObjectId(contract_id), {
        'event': 'rating: bhunter approved grade proof',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    })
    if result.acknowledged:
        return True
    return False


def prc_set_successful(contract_id):
    result = calls.c_submit_successful(ObjectId(contract_id), {
        'event': 'successful: both users have submitted their ratings',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    })
    if result.acknowledged:
        #  stuff to do...???
        return True
    return None


def prc_set_open(contract_id):
    result = calls.c_set_open(ObjectId(contract_id), {
        'event': 'contract set to \'open\'',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    })
    if result.acknowledged:
        #  stuff to do...???
        return True
    return None


def prc_submit_approval(contract_id):
    # bhunter gets paid
    # once paid, update database:
    result = calls.c_submit_approval(ObjectId(contract_id), {
        'event': 'assignment approved',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    })
    if result.acknowledged:
        #  stuff to do...
        return True
    return None


def prc_submit_gvalidation(contract_id, filename):
    result = calls.c_submit_gvalidation(ObjectId(contract_id), {
        'event': 'owner has submitted grade proof',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    }, filename)
    if result.acknowledged:
        return True
    return None


def prc_submit_assignment(contract_id, filename):
    result = calls.c_submit_assignment(ObjectId(contract_id), {
        'event': 'assignment submitted and waiting validation',
        'time': datetime.fromisoformat(datetime.now().isoformat())
    }, filename)
    if result.acknowledged:
        return True
    return None


def prc_submit_rating_c(comment, contract_id, rating, user_id):
    now_time = datetime.fromisoformat(datetime.now().isoformat())
    review_obj = {
        'comment': comment,
        'rating': float(rating),
        'time': now_time,
        'user': ObjectId(user_id)
    }
    rating_obj = calls.get_rating_obj(ObjectId(contract_id))
    if len(rating_obj['reviews']) == 0:
        result = calls.c_submit_rating_c(ObjectId(contract_id), review_obj)
        if result.matched_count > 0 and result.matched_count == result.modified_count:
            return True
    if len(rating_obj['reviews']) == 1:
        if rating_obj['reviews'][0]['user'] != ObjectId(user_id):
            # update contract reviews
            # rating submitted to contract
            result = calls.c_submit_rating_c(ObjectId(contract_id), review_obj)
            if result.matched_count > 0 and result.matched_count == result.modified_count:
                # user1 from passed in values
                user_review_obj1 = {
                    'comment': comment,
                    'contract': ObjectId(contract_id),
                    'rating': float(rating),
                    'reviewer': ObjectId(user_id),
                    'time': now_time
                }
                # user2 from rating_obj
                user_review_obj2 = {
                    'comment': rating_obj['reviews'][0]['comment'],
                    'contract': rating_obj['_id'],
                    'rating': float(rating_obj['reviews'][0]['rating']),
                    'reviewer': rating_obj['reviews'][0]['user'],
                    'time': now_time
                }
                other_user = rating_obj['bhunter']
                if other_user == ObjectId(user_id):
                    other_user = rating_obj['owner']
                result1a = calls.c_submit_rating_u(ObjectId(user_id), user_review_obj1)
                result1b = calls.c_submit_rating_u(ObjectId(user_id), user_review_obj2)
                result2a = calls.c_submit_rating_u(other_user, user_review_obj1)
                result2b = calls.c_submit_rating_u(other_user, user_review_obj2)
                result3 = calls.c_submit_successful(rating_obj['_id'], {
                    'event': 'successful: ratings submitted by both users',
                    'time': datetime.fromisoformat(datetime.now().isoformat())
                })
                if result1a.acknowledged and result1b.acknowledged and result2a.acknowledged and result2b.acknowledged and result3.acknowledged:
                    return True
                return None
            # update individual user reviewHistory for BOTH reviews
            # update phase of contract
    return None


# def prc_submit_successful(contract_id):
#     result = calls.c_submit_successful(ObjectId(contract_id), {
#         'event': 'successful: something about ratings being completed....',#HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#         'time': datetime.fromisoformat(datetime.now().isoformat()[:-7])
#     })
#     if result.acknowledged:
#         return True
#     return False


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
    #user_obj.update({"bhunter": ObjectId("000000000000000000000000")})
    user_obj.update({"bhunter": None})
    e_f_bonus = float(form_dict['c_f_efbonus'])
    user_obj.update({"efbonus": float(e_f_bonus)})
    e_g_bonus = float(form_dict['c_f_egbonus'])
    user_obj.update({"egbonus": float(e_g_bonus)})
    g_deadline = form_dict['c_f_t_g_deadline']
    if g_deadline != "":
        g_deadline = datetime.fromisoformat(form_dict['c_f_t_g_deadline'] + 'T' + form_dict['c_f_t_g_d_time'] + ':00.000000')
    lostudy = form_dict['c_f_lostudy']
    user_obj.update({"lostudy": lostudy})
    sampleText = form_dict['c_f_sample_str']
    if sampleText == '':
        user_obj.update({'sampleText': None})
    else:
        user_obj.update({"sampleText": sampleText})
    specialization = form_dict['c_f_specialization']
    user_obj.update({"specialization": specialization})
    stall_iso = datetime.fromisoformat(form_dict['c_f_t_stall'] + 'T' + form_dict['c_f_t_s_time'] + ':00')
    start_iso = datetime.fromisoformat(datetime.now().isoformat())
    user_obj.update({"clog": []})
    subject = form_dict['c_f_subject']
    user_obj.update({"subject": subject})
    type_contract = form_dict['c_f_type']
    user_obj.update({"type_contract": type_contract})
    instructions = form_dict['c_f_instructions']
    user_obj.update({'instructions': instructions})
    # set up assignment contract:
    if type_contract == 'assignment':
        a_deadline_iso = datetime.fromisoformat(form_dict['c_f_t_a_deadline'] + 'T' + form_dict['c_f_t_a_d_time'] + ':00')
        if e_f_bonus != 0.0:
            efbonus_deadline = datetime.fromisoformat(form_dict['c_f_efb_deadline'] + 'T' + form_dict['c_f_efb_d_time'] + ':00')
            user_obj.update({'timeline': [{'time': start_iso, 'event': "created"},
                                          {'time': stall_iso, 'event': "deadline: stall"},
                                          {'time': a_deadline_iso, 'event': "deadline: submission"},
                                          {'time': g_deadline, 'event': "deadline: grading"},
                                          {'time': g_deadline, 'event': "deadline: rate the other person"},
                                          {'time': efbonus_deadline, 'event': "deadline: early finish bonus!"}]})  # MISSING CORRECT RATING DEADLINE
        else:
            user_obj.update({'timeline': [{'time': start_iso, 'event': "created"},
                                      {'time': stall_iso, 'event': "deadline: stall"},
                                      {'time': a_deadline_iso, 'event': "deadline: submission"},
                                      {'time': g_deadline, 'event': "deadline: grading"},
                                      {'time': g_deadline, 'event': "deadline: rate the other person"}]})# MISSING CORRECT RATING DEADLINE
    # set up assignment contract:
    if type_contract == 'test':
        t_start_iso = datetime.fromisoformat(form_dict['c_f_t_t_start'] + 'T' + form_dict['c_f_t_t_s_time'] + ':00')
        t_end_iso = datetime.fromisoformat(form_dict['c_f_t_t_end'] + 'T' + form_dict['c_f_t_t_e_time'] + ':00')
        user_obj.update({'timeline': [{'time': start_iso, 'event': "created"},
                                      {'time': stall_iso, 'event': "deadline: stall"},
                                      {'time': t_start_iso, 'event': "deadline: test start"},
                                      {'time': t_end_iso, 'event': "deadline: test end"},
                                      {'time': g_deadline, 'event': "deadline: grading"},
                                      {'time': g_deadline, 'event': "deadline: rate the other person"}]})# MISSING CORRECT RATING DEADLINE
    # add in data not initiated by user:
    user_obj.update({'owner': userid})
    user_obj.update({'iparties': []})
    user_obj.update({"clog": [{'event': "created", 'time': start_iso}]})
    user_obj.update({'phase': "creation"})
    user_obj.update({'reviews': []})
    user_obj.update({'chat': []})
    user_obj.update({'lvbhunter': None})
    user_obj.update({'lvowner': None})
    user_obj.update({'sampleUp': None})
    user_obj.update({'asubmission': None})
    user_obj.update({'gsubmission': None})
    c_insert_return = calls.create_contract(user_obj)
    return c_insert_return


def process_new_user(email, password1, username):
    user_template = {
        'active': True,
        'email': email,
        'pass': generate_password_hash(password1),
        'uName': username,
        'joinDate': datetime.fromisoformat(datetime.now().isoformat()),
        'timezone': 'sometimezonezzz',
        'reviewHistory': []
    }
    return calls.create_user(user_template)


def process_user_orders(userid_obj):
    cursor_obj = calls.get_user_contracts(userid_obj)
    if cursor_obj:
        obj_arr = []
        for doc in cursor_obj:
            obj_arr.append(doc)
        return obj_arr
    else:
        return None


if __name__ == '__main__':
    print(get_user_record('theman@gmail.com', 'passwordpass'))