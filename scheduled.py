from pymongo import MongoClient, DESCENDING
from datetime import datetime
from bson.objectid import ObjectId


dbContracts = 'ab_dbcontracts'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
db_mc = MongoClient()
ccontracts = "ccontracts"
cusers = "cusers"


def move_stalled():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.fromisoformat(datetime.now().isoformat()[:-7])
    contracts = list(dbc.find({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'event': 'deadline: stall'}}}, {'timeline': {'$elemMatch': {'$lte': {'time': nowtime}}}}]}))
    if len(contracts) > 0:
        # holds list of all users that were changed:
        stalled_arr = []
        for obj in contracts:
            stalled_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'$lte': {'time': nowtime}}}}]}, {'$set': {'phase': 'stalled'}, '$push': {'clog': {'event': 'contract stalled', 'time': nowtime}}})
        if contracts.acknowledged:
            # send alerts to all users that have had their contracts stall
            # owner forfeits processing fees
            return [contracts, stalled_arr]
        return ["error during update"]
    return ["nothing to update"]

if __name__ == '__main__':
    print(move_stalled(), '\n')
    # print(user_loader("theman@gmail.com"))