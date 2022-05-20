'''
Alex Haas
functions that make the calls and then separate functions that prepare data for use by FE
'''
from werkzeug.security import check_password_hash
from pymongo import MongoClient, DESCENDING
import datetime


dbOrders = 'ab_dborders'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
db_mc = MongoClient()
corders = "corders"
cusers = "cusers"


dict_template = {
                'active': True,
                'email': 'aaaa@aaaa.com',
                'pass': 'aaaassssddddffff',
                'uName': 'somename',
                'joinDate': 'some date for sure 2',
                'orders': []
            }
'''
INCOMPLETE
'''
def create_user(user_obj):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    print(user_obj['email'])
    result = dbc.find_one({'email': user_obj['email']})
    if result:
        return False
    else:
        dbc.insert_one(user_obj)
        return True


'''
INCOMPLETE
'''
def get_active(email):
    db = db_mc[dbOrders]
    dbc = db[cusers]
    temp_obj = dbc.find_one({'email': email})
    if temp_obj:
        return True
    else:
        return False


'''
INCOMPLETE
'''
def get_orders_top():
    db = db_mc[dbOrders]
    dbc = db[corders]
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
def get_user_record_email(email):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"email": email})#need to add a filter?
    if user_record:
        return user_record
    else:
        return None


'''
INCOMPLETE
'''
def get_username(email):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    username = dbc.find_one({'email': email}, {
        '_id': 0,
        'uName': 1
    })
    if username:
        return username['uName']
    else:
        return None


'''
INCOMPLETE
returns object if True, None if False
'''
def is_auth_user(email, password):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"email": email}, {
        '_id': 0,
        'email': 1,
        'uName': 1,
        'pass': 1
    })
    if user_record and check_password_hash(user_record['pass'], password):
        user_record.pop('pass')
        return user_record
    else:
        return None


if __name__ == '__main__':
    print(create_user(dict_template))
