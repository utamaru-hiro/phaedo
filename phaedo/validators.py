import re
from .core.validation import Validator


def mandatory():
    return Validator(lambda v: v is not None, '必須項目です')


def max_length(length: int):
    return Validator(lambda v: v is None or len(v) <= length, f'{length}文字以下で入力してください')


def min_length(length: int):
    return Validator(lambda v: v is None or len(v) >= length, f'{length}文字以上で入力してください')


def regex(pattern: str):
    return Validator(lambda v: v is None or re.match(pattern, v), '不正な値です')


def url():
    return regex(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')


def mailaddress():
    return regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def value_in(values: list):
    return Validator(lambda v: v is None or v in values, '不正な値です')
