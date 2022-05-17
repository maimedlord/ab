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
def get_user_record(email, pass_word):
    db = db_mc[dbUsers]
    dbc = db[cusers]
    user_record = dbc.find_one({"email": email, "pass": pass_word})
    if user_record:
        return user_record
    else:
        return {"error": "no record found"}


if __name__ == '__main__':
    print(get_user_record('theman@gmail.com', 'passwordpass'))