from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta
from bson.objectid import ObjectId


dbContracts = 'ab_dbcontracts'
dbUsers = 'ab_dbusers'
dbSiteGen = 'ab_dbsitegen'
dbGames = 'ab_dbgames'
db_mc = MongoClient()
ccontracts = 'ccontracts'
cusers = 'cusers'


def failed_a_submit():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'inprogress'},
                                        {'type_contract': 'assignment'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: submission', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        # holds list of all users that will be changed:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'inprogress'},
                                              {'type_contract': 'assignment'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: submission', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'disputed'}, '$push': {'clog': {'event': 'disputed: failed assignment submission', 'time': nowtime}}})
        if contracts.acknowledged:
            # stuff???
            return [contracts, failed_arr]
        return ['failed_a_submit: error during update']
    return ['failed_a_submit: nothing to update']


def failed_g_submit():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'approved'},
                                        {'type_contract': 'assignment'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: grading', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'approved'},
                                              {'type_contract': 'assignment'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: grading', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'rating'}, '$push': {'clog': {'event': 'rating: failed assignment grade submission', 'time': nowtime}}})
        if contracts.acknowledged:
            return [contracts, failed_arr]
        return ['failed_g_submit: error during update']
    return ['failed_g_submit: nothing to update']


def failed_a_validation():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    nowtimeplus24 = nowtime + timedelta(hours=24)
    contracts = list(dbc.find({'$and': [{'phase': 'validation'},
                                        {'type_contract': 'assignment'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: submission', 'time': {'$lte': nowtimeplus24}}}}]}))
    if len(contracts) > 0:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'validation'},
                                              {'type_contract': 'assignment'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: submission', 'time': {'$lte': nowtimeplus24}}}}]},
                                    {'$set': {'phase': 'approved'}, '$push': {'clog': {'event': 'approved: failed assignment validation', 'time': nowtime}}})
        if contracts.acknowledged:
            return [contracts, failed_arr]
        return ['failed_a_validation: error during update']
    return ['failed_a_validation: nothing to update']


def failed_t_validation():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'validation'},
                                        {'type_contract': 'test'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: test start', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'validation'},
                                              {'type_contract': 'test'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: test start', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'disputed'}, '$push': {'clog': {'event': 'disputed: owner did not validate bhunter\'s performance', 'time': nowtime}}})
        if contracts.acknowledged:
            return [contracts, failed_arr]
        return ['move_t_validation: error during update']
    return ['move_t_validation: nothing to update']


def failed_rating():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'rating'},
                                        {'type_contract': 'assignment'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: rate the other person', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'rating'},
                                              {'type_contract': 'assignment'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: rate the other person', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'successful'}, '$push': {'clog': {'event': 'successful: failed rating', 'time': nowtime}}})
        if contracts.acknowledged:
            return [contracts, failed_arr]
        return ['failed_rating: error during update']
    return ['failed_rating: nothing to update']


def move_stalled():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'open'}, {'timeline': {'$elemMatch': {'event': 'deadline: stall', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        # holds list of all users that will be changed:
        stalled_arr = []
        for obj in contracts:
            stalled_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'open'},
                                              {'timeline': {'$elemMatch': {'event': 'deadline: stall', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'stalled'}, '$push': {'clog': {'event': 'stalled: failed deadline', 'time': nowtime}}})
        if contracts.acknowledged:
            # send alerts to all users that have had their contracts stall
            # owner forfeits processing fees
            return [contracts, stalled_arr]
        return ['moved_stalled: error during update']
    return ['move_stalled: nothing to update']


def move_t_validation():
    db = db_mc[dbContracts]
    dbc = db[ccontracts]
    nowtime = datetime.utcnow()
    contracts = list(dbc.find({'$and': [{'phase': 'inprogress'},
                                        {'type_contract': 'test'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: test start', 'time': {'$lte': nowtime}}}}]}))
    if len(contracts) > 0:
        failed_arr = []
        for obj in contracts:
            failed_arr.append({'ownerid': obj['owner'], 'contractid': obj['_id']})
        contracts = dbc.update_many({'$and': [{'phase': 'inprogress'},
                                        {'type_contract': 'test'},
                                        {'timeline': {'$elemMatch': {'event': 'deadline: test start', 'time': {'$lte': nowtime}}}}]},
                                    {'$set': {'phase': 'validation'}, '$push': {'clog': {'event': 'validation: test has started', 'time': nowtime}}})
        if contracts.acknowledged:
            return [contracts, failed_arr]
        return ['move_t_validation: error during update']
    return ['move_t_validation: nothing to update']


if __name__ == '__main__':
    print(move_t_validation(), '\n')
    # print(user_loader("theman@gmail.com"))