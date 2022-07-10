'''
Alex Haas
functions that make the calls and then separate functions that prepare data for use by FE
'''
from werkzeug.security import check_password_hash
from pymongo import MongoClient, DESCENDING, ReturnDocument
from datetime import datetime
from bson.objectid import ObjectId


dbContracts = 'ab_dbcontracts'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
dbLogs = 'ab_dblogs'
dbUploads = 'ab_dbuploads'
db_mc = MongoClient()
ccontracts = 'ccontracts'
cusers = 'cusers'
login_log = 'loginlog'
logout_log = 'logoutlog'
samples = 'samples'


dict_template = {
                'active': True,
                'email': 'aaSDaa@aaaSDa.com',
                'pass': 'aaaassssddddffff',
                'uName': 'somename',
                'joinDate': 'some date for sure 2',
                'orders': []
            }


def c_accept_offer(contractid_obj, bhunterid_obj, bhunter_offer, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    result = dbc.update_one({'_id': contractid_obj},
                            {'$set': {'bhunter': bhunterid_obj, 'phase': 'inprogress', 'bounty': bhunter_offer},
                             '$push': {'clog': clog_obj}})
    return result


def c_create_ip(contract_id, ip_object):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$push': {'iparties': ip_object}})


def c_send_chat(contractid_obj, chat_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contractid_obj}, {'$push': {'chat': chat_obj}})


def cancel_contract(contract_id):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.delete_one({'_id': ObjectId(contract_id)})


def create_contract(user_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    # check if user exists
    if dbc.find_one(user_obj['owner']):
        db = db_mc[dbContracts]
        dbc = db[ccontracts]
        result = dbc.insert_one(user_obj)
        return result
    return None


def create_user(user_template):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    email_result = dbc.find_one({'email': user_template['email']})
    username_result = dbc.find_one({'uName': user_template['uName']})
    if email_result or username_result:
        return False
    else:
        dbc.insert_one(user_template)
        return True


def get_all_open():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    contract_cursor = dbc.find({'phase': 'open'})
    if contract_cursor:
        return list(contract_cursor)
    return None


'''
INCOMPLETE
returns object if True, None if False
'''


def get_auth_user(email, password):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"email": email}, {
        '_id': 1,
        'email': 1,
        'uName': 1,
        'pass': 1
    })
    if user_record and check_password_hash(user_record['pass'], password):
        # remove password from the object before returning:
        user_record.pop('pass')
        return [str(user_record['_id']), email, user_record['uName'], user_record['_id']]
    else:
        return None


# returns contract or None
def c_get_contract(contract_id):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.find_one({'_id': ObjectId(contract_id)})


# MAKE THIS USE ONE QUERY WITH AGGREGATION... MAYBE BATCHES?
def c_get_contract_account(contract_id, nowtime, user_id):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    # AGGREGATION ...
    # result =  dbc.find_one_and_update({'_id': contract_id},
    #                                [{'$bucket': {
    #                                    '$groupBy': 'owner',
    #                                }}])
    # print(result)
    # return result


def get_contracts_top_10():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    contract_cursor = dbc.find({'phase': 'open'}).limit(10)
    if contract_cursor:
        return contract_cursor
    return None


def get_rating_obj(contract_id):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.find_one({'_id': contract_id}, {
        '_id': 1,
        'bhunter': 1,
        'owner': 1,
        'reviews': 1
    })


def get_sesh(userid):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"_id": ObjectId(userid)}, {
        '_id': 1,
        'email': 1,
        'uName': 1
    })
    if user_record:
        temp_array = [userid, user_record['email'], user_record['uName'], user_record['_id']]
        return temp_array
    else:
        return []


def get_user(user_id):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({'_id': ObjectId(user_id)}, {
        'pass': 0
    })# add filter?
    return user_record


def get_user_contracts(userid_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    user_orders = dbc.find({"$or": [{"owner": userid_obj}, {"bhunter": userid_obj},
                                    {'$and': [{'phase': 'open'}, {'iparties.bhunter': userid_obj}]}]})
    return user_orders


def get_username(userid_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_name = dbc.find_one({'_id': ObjectId(userid_obj)}, {
        'uName': 1
    })
    return user_name


def c_set_disputed(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'disputed'}, '$push': {'clog': clog_obj}})


def c_set_sampleUp(contract_id, loc_string):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': ObjectId(contract_id)}, {'$set': {'sampleUp': loc_string}})


def c_submit_approval(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'approved'}, '$push': {'clog': clog_obj}})


def c_submit_successful(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'successful'}, '$push': {'clog': clog_obj}})


def c_getset_lvbhunter(contract_id, time):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.find_one_and_update({'_id': contract_id}, {'$set': {'lvbhunter': time}})


def c_getset_lvowner(contract_id, time):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.find_one_and_update({'_id': contract_id}, {'$set': {'lvowner': time}})


def c_set_open(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'open'}, '$push': {'clog': clog_obj}})


def c_set_rating(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'rating'}, '$push': {'clog': clog_obj}})


def c_submit_gvalidation(contract_id, clog_obj, filename):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    result = dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'gradevalidation', 'gsubmission': filename}, '$push': {'clog': clog_obj}})
    return result


def c_submit_assignment(contract_id, clog_obj, filename):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$set': {'phase': 'validation', 'asubmission': filename}, '$push': {'clog': clog_obj}})


def c_submit_rating_c(contract_id, review_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$push': {'reviews': review_obj}})


def c_submit_rating_u(user_id, review_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    return dbc.update_one({'_id': user_id}, {'$push': {'reviewHistory': review_obj}})


def c_update_clog(contract_id, clog_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$push': {'clog': clog_obj}})


def check_size():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    print(dbc.stats())


def log_userlogin(user_id):
    db = db_mc[dbLogs]
    dbc = db[login_log]
    result = dbc.insert_one({
        'time': datetime.fromisoformat(datetime.now().isoformat()),
        'userid': user_id
    })
    if result.acknowledged:
        print(str(user_id) + ' has logged in')
    else:
        print('failed to log user login for ' + str(user_id))


def log_userlogout(user_id):
    db = db_mc[dbLogs]
    dbc = db[logout_log]
    result = dbc.insert_one({
        'time': datetime.fromisoformat(datetime.now().isoformat()),
        'userid': user_id
    })
    if result.acknowledged:
        print(str(user_id) + ' has logged out')
    else:
        print('failed to log user logout for ' + str(user_id))


def upload_sample(sample_obj):
    db = db_mc[dbUploads]
    dbc = db[samples]
    return dbc.insert_one(sample_obj)
