'''
Alex Haas
functions that make the calls and then separate functions that prepare data for use by FE
'''
from pymongo import MongoClient, DESCENDING
import datetime


dbOrders = 'ab-dborders'
dbUsers = 'ab-dbusers'
dbSiteGen = 'ab-dbsitegen'
dbGames = 'ab-dbgames'
db_mc = MongoClient()


'''
Which ones will be chosen?
'''
def get_orders_top():
    db = db_mc[dbOrders]
    dbc = db["corders"]
    mongo_obj = dbc.find_one(sort=[('_id', DESCENDING)])
    some_str = mongo_obj.get("status")
    return some_str