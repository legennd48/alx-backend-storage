#!/usr/bin/env python3
'''
10. Change school topics
'''


def update_topics(mongo_collection, name, topics):
    '''
    changes all topics of a school
    document based on name
    '''

    if mongo_collection is not None:
        mongo_collection.update_many(
            {'name': name},
            {'$set': {'topics': topics}}
         )
