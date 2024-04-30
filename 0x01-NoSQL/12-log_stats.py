#!/usr/bin/env python3
'''
Analyzes Nginx logs stored in MongoDB
and displays statistics.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """
    Prints statistics about Nginx request logs.

    Args:
        nginx_collection (pymongo.collection.Collection):
        The MongoDB collection containing Nginx request logs.
    """

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        req_count = len(list(nginx_collection.find({"method": method})))
        print(f"\tmethod {method}: {req_count}")

    status_checks_count = len(
        list(nginx_collection.find({"method": "GET", "path": "/status"}))
    )
    print(f"{status_checks_count} status check")


def run():
    """
    Connects to MongoDB, retrieves statistics, and prints them.
    """

    client = MongoClient("mongodb://127.0.0.1:27017")
    print_nginx_request_logs(client.logs.nginx)


if __name__ == "__main__":
    run()
