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


def create_user(user_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    print(user_obj['email'])
    email_result = dbc.find_one({'email': user_obj['email']})
    username_result = dbc.find_one({'uName': user_obj['uName']})
    if email_result or username_result:
        return False
    else:
        dbc.insert_one(user_obj)
        return True


'''
INCOMPLETE
'''


def get_active(email):
    db = db_mc[dbContracts]
    dbc = db[cusers]
    temp_obj = dbc.find_one({'email': email})
    if temp_obj:
        return True
    else:
        return False

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
        #user_record.pop('pass')
        tstring = str(user_record['_id'])
        temp_array = [tstring, email, user_record['uName'], user_record['_id']]
        return temp_array
    else:
        return []


'''
INCOMPLETE
'''


def get_orders_top():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    temp_array = list(dbc.find({}, {
        "_id": 0,
        "orderID": 1,
        "dateOpen": 1,
        "level": 1,
        "subject": 1,
        "status": 1,
        "contract.commitment": 1,
        "contract.finalPrice": 1
    }).limit(5))
    return temp_array


'''
INCOMPLETE
'''


def get_sesh(id):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"_id": ObjectId(id)}, {
        '_id': 1,
        'email': 1,
        'uName': 1
    })
    if user_record:
        temp_array = [id, user_record['email'], user_record['uName'], user_record['_id']]
        return temp_array
    else:
        return []


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