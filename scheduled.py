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


'''
INCOMPLETE
'''


def move_stalled():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.fromisoformat(datetime.now().isoformat()[:-7])
    contracts = list(dbc.find({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'event': 'deadline: stall'}}}, {'timeline': {'$elemMatch': {'$gt': {'time': nowtime}}}}]}))# {'bounty': {'$gt': 400}} dbc.find({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'event': 'deadline: stall'}}}]})
    if len(contracts) > 0:
        stalled_obj = []
        for obj in contracts:
            stalled_obj.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'event': 'deadline: stall'}}}, {'timeline': {'$elemMatch': {'$lte': {'time': nowtime}}}}]}, {'$set': {'phase': 'stalled'}, '$push': {'clog': {'event': 'contract moved to stalled', 'time': nowtime}}})
        if contracts.matched_count > 0 and contracts.matched_count == contracts.modified_count and len(stalled_obj) > 0:
            # now that the change has been made and the contracts in question stored in stalled_obj, an alert needs to be generated that moves the contract onward...
            return [contracts, stalled_obj]
        return ["error during update"]
    return ["nothing to update"]

if __name__ == '__main__':
    print(move_stalled(), '\n')
    # print(user_loader("theman@gmail.com"))