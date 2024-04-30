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

    students = []
    for student in mongo_collection.find():
        scores = student.get("scores", [])
        if scores:
            average_score = mean(scores)
            student["averageScore"] = average_score
            students.append(student)

    return sorted(students, key=lambda x: x["averageScore"], reverse=True)
