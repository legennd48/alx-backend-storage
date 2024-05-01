#!/usr/bin/env python3
'''
9. Insert a document in Python
'''


def insert_school(mongo_collection, **kwargs):
    '''
    Function inserts a new document into a collection
    Args:
    - mongo_collection: a pymongo collection object
    - kwargs: keyword arguments representing the fields
    and values of the document to be inserted
    Returns:
    - The _id of the inserted document
    '''

    if mongo_collection is not None:
        return mongo_collection.insert_one(kwargs).inserted_id
