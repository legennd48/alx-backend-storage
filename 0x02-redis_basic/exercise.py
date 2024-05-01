#!/usr/bin/env python3
'''
Radis NoSQL storage
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """
    Decorator that tracks the number of calls made to a
    method in a Cache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method with call counting functionality.
    """

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its call counter in Redis.

        Args:
            self: The Cache object instance.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The return value of the decorated method.
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return invoker


def call_history(method: Callable) -> Callable:
    """
    Decorator that tracks the call history of a method in a Cache class.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method with call history
        tracking functionality.
    """

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the method, stores its inputs and output in Redis,
        and returns the output.

        Args:
            self: The Cache object instance.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The return value of the decorated method.
        """

        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output

    return invoker


def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class' method.

    Args:
        fn (Callable): The method whose call history needs to be displayed.
    """

    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """
    Represents a cache object for storing data in a Redis data storage.

    This class provides methods for storing and retrieving data from Redis,
    with functionalities for tracking method call counts and call history.
    """

    def __init__(self) -> None:
        """
        Initializes a Cache instance and establishes a Redis connection.

        The Redis instance is flushed upon initialization to
        clear any existing data.
        """

        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used to store the data.
        """

        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage.

        Args:
            key (str): The key associated with the data to be retrieved.
            fn (Callable, optional): A function to apply to the retrieved data.
                Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data,
            optionally transformed by the provided function.
        """

        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.

        Args:
            key (str): The key associated with the string data to be retrieved.

        Returns:
            str: The retrieved string data.
        """

        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.

        Args:
            key (str): The key associated with the integer
            data to be retrieved.

        Returns:
            int: The retrieved integer data.
        """

        return self.get(key, lambda x: int(x))
