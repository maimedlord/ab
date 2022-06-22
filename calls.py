'''
Alex Haas
functions that make the calls and then separate functions that prepare data for use by FE
'''
from werkzeug.security import check_password_hash
from pymongo import MongoClient, DESCENDING
import datetime
from bson.objectid import ObjectId


dbContracts = 'ab_dbcontracts'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
db_mc = MongoClient()
ccontracts = "ccontracts"
cusers = "cusers"


dict_template = {
                'active': True,
                'email': 'aaSDaa@aaaSDa.com',
                'pass': 'aaaassssddddffff',
                'uName': 'somename',
                'joinDate': 'some date for sure 2',
                'orders': []
            }

'''
INCOMPLETE
'''


def create_contract(user_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    print(user_obj)
    # check if user exists
    if dbc.find_one(user_obj['owner']):
        db = db_mc[dbContracts]
        dbc = db[ccontracts]
        result = dbc.insert_one(user_obj)
        print("yups")
        print(result)
    #result = dbc.insert_one(user_obj)
    return None


'''
INCOMPLETE
'''


def create_user(user_template):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    print(user_template['email'])
    email_result = dbc.find_one({'email': user_template['email']})
    username_result = dbc.find_one({'uName': user_template['uName']})
    if email_result or username_result:
        return False
    else:
        dbc.insert_one(user_template)
        return True


# '''
# INCOMPLETE
# '''
#
#
# def get_active(email):
#     db = db_mc[dbContracts]
#     dbc = db[cusers]
#     temp_obj = dbc.find_one({'email': email})
#     if temp_obj:
#         return True
#     else:
#         return False

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
        user_record.pop('pass')
        tstring = str(user_record['_id'])
        temp_array = [tstring, email, user_record['uName'], user_record['_id']]
        return temp_array
    else:
        return []


'''
INCOMPLETE
need to add filter to reduce returned data
'''


def get_contract(contract_id):
    print(contract_id)
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    contract_obj = dbc.find_one({'_id': ObjectId(contract_id)})
    print(contract_obj)
    if contract_obj:
        dict(contract_obj)
    return contract_obj


'''
INCOMPLETE
'''


def get_contracts_top_10():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    contract_cursor = dbc.find().limit(10)
    if contract_cursor:
        return contract_cursor
    return None


'''
INCOMPLETE
'''


def get_all_open():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    contract_cursor = dbc.find({'phase': 'open'})
    if contract_cursor:
        return list(contract_cursor)
    return None


'''
INCOMPLETE
'''


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


'''
INCOMPLETE
'''


def get_user_contracts(userid_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    user_orders = dbc.find({"$or": [{"owner": userid_obj}, {"bhunter": userid_obj}]})
    # print(user_orders)
    # for doc in user_orders:
    #     print(doc)
    return user_orders


'''
INCOMPLETE
add filter to returned object???
'''


def get_user(userid_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({'_id': ObjectId(userid_obj)}, {
        'pass': 0
    })# add filter?
    return user_record


'''
INCOMPLETE
'''


def get_username(userid_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_name = dbc.find_one({'_id': ObjectId(userid_obj)}, {
        'uName': 1
    })
    return user_name


'''
INCOMPLETE
'''


def create_ip(contract_id, ip_object):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    return dbc.update_one({'_id': contract_id}, {'$push': {'iparties': ip_object}})


'''
INCOMPLETE
'''


def update_inprogress(contractid_obj, bhunterid_obj):
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    result = dbc.update_one({'_id': contractid_obj}, {'$set': {'bhunter': bhunterid_obj, 'phase': 'inprogress'}})
    print(result)
    pass


# '''
# INCOMPLETE
# '''
# def get_username(email):
#     db = db_mc[dbUsers]
#     dbc = db[cusers]
#     username = dbc.find_one({'email': email}, {
#         '_id': 0,
#         'uName': 1
#     })
#     if username:
#         return username['uName']
#     else:
#         return None


if __name__ == '__main__':
    print(create_user(dict_template))
