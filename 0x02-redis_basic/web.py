#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Decorator that caches the output of a function that
    fetches data from a URL.

    This decorator tracks the number of times the decorated function is called
    for a specific URL and caches the fetched data for a configurable duration.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with caching and
        tracking capabilities.
    """

    @wraps(method)
    def invoker(url: str) -> str:
        """
        Retrieves the content of a URL, caches the response,
        and tracks the request.

        Args:
            url (str): The URL of the webpage to fetch.

        Returns:
            str: The content of the fetched webpage.
        """

        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')

        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)  # Cache for 10 seconds
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Fetches the content of a webpage, caches the response for 10 seconds, and
    tracks the number of times the request is made.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The content of the fetched webpage.
    """

    return requests.get(url).text
