#!/usr/bin/env python3
'''
14. Top students
'''
from statistics import mean


def top_students(mongo_collection):
    """
    Returns all students from the collection
    sorted by their average score.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection containing student data.

    Returns:
        list: A list of dictionaries representing students,
        each with an "averageScore" key added.
    """

    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return students
