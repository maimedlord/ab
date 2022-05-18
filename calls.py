'''
Alex Haas
functions that make the calls and then separate functions that prepare data for use by FE
'''
from pymongo import MongoClient, DESCENDING
import datetime


dbOrders = 'ab_dborders'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
db_mc = MongoClient()
corders = "corders"
cusers = "cusers"


'''
'''
def is_user(email, hashed_password):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"email": email, "pass": hashed_password})  # need to add a filter?
    if user_record:
        return True
    else:
        return False


'''
'''
def get_active(email):
    db = db_mc[dbOrders]
    dbc = db[cusers]
    temp_obj = dbc.find_one({"email": email})
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


if __name__ == '__main__':
    print(get_user_record_email("theman@gmail.com"))
    print(type(get_user_record_email("theman@gmail.com")))
