import typing
import types
from typing import *
from types import *
import io
import abc
import collections
import contextlib

def is_io_instance(obj, tp) -> bool:
    """
    >>> with open("example.txt", "r") as text_file:
    ...     print(is_io_instance(text_file, IO))  # Output: True
    ...     print(is_io_instance(text_file, IO[str]))  # Output: True
    ...     print(is_io_instance(text_file, IO[bytes]))  # Output: False
    True
    True
    False

    >>> with open("example.bin", "rb") as binary_file:
    ...     print(is_io_instance(binary_file, IO))  # Output: True
    ...     print(is_io_instance(binary_file, IO[str]))  # Output: False
    ...     print(is_io_instance(binary_file, IO[bytes]))  # Output: True
    True
    False
    True
    """
    origin = get_origin(tp)
    args = get_args(tp)

    if origin and issubclass(origin, IO):
        assert args
        if args[0] == str:
            return isinstance(obj, io.TextIOBase)
        elif args[0] == bytes:
            return isinstance(obj, io.BufferedIOBase)

    if isinstance(tp, type) and issubclass(tp, IO):
        return isinstance(obj, io.IOBase)

    return False


def func(x: int, y: str):
    return "Hello"

required_type = Callable[[int, str], None]

def is_callable_instance(obj, tp) -> bool:
    if not callable(obj):
        return False

    if not hasattr(tp, "__args__") or len(tp.__args__) != 2:
        print(tp.__args__)
        raise ValueError("Expected a Callable with two type arguments")

    arg_types, return_type = tp.__args__

    type_hints = get_type_hints(obj)
    if "return" not in type_hints:
        return False

    if type_hints["return"] != return_type:
        return False

    signature = list(type_hints.items())[:-1]
    if len(signature) != len(arg_types):
        return False

    for i, (arg_name, arg_type) in enumerate(signature):
        if arg_type != arg_types[i]:
            return False

    return True

# print(is_callable_instance(func, required_type))  # True

print(required_type.__args__)
