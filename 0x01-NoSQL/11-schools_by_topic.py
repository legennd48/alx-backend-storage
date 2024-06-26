#!/usr/bin/env python3
'''
11. Where can I learn Python?
'''


def schools_by_topic(mongo_collection, topic):
    '''
    returns the list of school having a specific topic:
    '''
    filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(filter)]
