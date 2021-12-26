from typing import Any, Callable


class ValidationError(Exception):
    def __init__(self, key: str, message: str = ''):
        self._message = f'{key}: {message}'

    def __str__(self) -> str:
        return self._message


class Validator:
    def __init__(self, test: Callable[[Any], bool], message: str):
        self._test = test
        self._message = message

    def validate(self, v) -> bool:
        return self._test(v)

    def message(self):
        return self._message
