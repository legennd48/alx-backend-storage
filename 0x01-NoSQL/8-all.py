#!/usr/bin/env python3
'''
8. List all documents in Python
'''


def list_all(mongo_collection):
    '''
    function lists all documents in a collection
    args:
    mongo_collection - pymongo collection object
    return:
    list of documents in collection
    '''

    if (mongo_collection is not None):
        docs =  mongo_collection.find()
        return [x for x in docs]
        
    return []
