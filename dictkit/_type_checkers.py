import typing
import types
from typing import *
from types import *
import io

# import abc
import collections
import contextlib
from collections import abc


def validate(obj, tp) -> bool:
    """
    The main driver of type checking.
    1. Figure out what check function to call (if any) based on the value of `tp`
    2. Call that function, which will then call back up to this function recursively
       for each nested layer of arguments.
    3. Get back a boolean, and actually raise an error if False
    4. Return True
    """

    if (tp is None or tp == NoneType) and obj != None:
        return False

    if tp is type and not type(obj) == type:
        return False

    origin = get_origin(tp)

    if origin is None:
        return check_when_no_origin(obj, tp)
    if origin in {UnionType, Union}:
        return any(validate(obj, arg) for arg in get_args(tp))
    if origin == abc.Iterable:
        return is_iterable_instance(obj, tp)
    if origin == list:
        return is_list_instance(obj, tp)
    if origin == tuple:
        return is_tuple_instance(obj, tp)
    if origin == dict:
        return is_dict_instance(obj, tp)
    if origin in {set, frozenset}:
        return is_set_instance(obj, tp)
    if origin == Callable:
        return is_callable_instance(obj, tp)
    if origin == IO:
        return is_io_instance(obj, tp)

    return False


def check_when_no_origin(obj, tp) -> bool:
    return isinstance(obj, tp)


def is_iterable_instance(obj, tp) -> bool:
    if not (args := get_args(tp)):
        return isinstance(obj, Iterable)
    if not isinstance(obj, Iterable):
        return False
    return all(validate(elem, args[0]) for elem in obj)


def is_list_instance(obj, tp) -> bool:
    if not isinstance(obj, list):
        return False
    elem_tp = get_args(tp)[0]
    return all(validate(elem, elem_tp) for elem in obj)


def is_set_instance(obj, tp) -> bool:
    if not isinstance(obj, set):
        return False
    elem_tp = get_args(tp)[0]
    return all(validate(elem, elem_tp) for elem in obj)


def is_tuple_instance(obj, tp) -> bool:
    if not isinstance(obj, tuple):
        return False

    args = get_args(tp)

    if len(args) == 2 and args[1] == ...:
        return all(validate(elem, args[0]) for elem in obj)

    if len(obj) != len(args):
        return False

    return all(validate(elem, arg) for elem, arg in zip(obj, args))


def is_dict_instance(obj, tp) -> bool:
    if not isinstance(obj, dict):
        return False

    args = get_args(tp)
    key_arg, val_arg = args

    return all(
        validate(k, key_arg) and validate(v, val_arg)
        for k, v in obj.items()
    )


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
    origin, args = get_origin(tp), get_args(tp)

    if origin and issubclass(origin, IO):
        assert args
        if args[0] == str:
            return isinstance(obj, io.TextIOBase)
        elif args[0] == bytes:
            return isinstance(obj, io.BufferedIOBase)

    if isinstance(tp, type) and issubclass(tp, IO):
        return isinstance(obj, io.IOBase)

    return False


def func1(x: int, y: str) -> list:
    return ["Hello"]


def func2(x: str):
    return


def func3() -> int:
    return 5


def func4(a, b, c, d) -> int:
    return 5


def func5(a, b, c, d):
    return 5


t1 = Callable[[int, str], list]
t2 = Callable[[str], None]
t3 = Callable[[], int]
t4 = Callable


def is_callable_instance(obj, tp) -> bool:
    assert get_origin(tp) == Callable
    if not callable(obj):
        return False

    args, hints = get_args(tp), get_type_hints(obj)
    if not args:
        return True
    if not hints or "return" not in hints:
        return False  # We know there are args, so there must be hints with return

    args_param, arg_return = args[:-1], args[-1]
    hints_param, hint_return = [v for k, v in hints.items() if k != "return"], hints[
        "return"
    ]

    if not arg_return == hint_return:
        return False
    if args_param:
        if len(args_param) != len(hints_param):
            return False
        for expected, got in zip(args_param, hints_param):
            if not expected == got:
                return False

    return True
