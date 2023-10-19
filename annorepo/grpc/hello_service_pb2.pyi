from typing import ClassVar as _ClassVar, Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor


class SayHelloRequest(_message.Message):
    __slots__ = ["name", "api_key"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    name: str
    api_key: str

    def __init__(self, name: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...


class SayHelloResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str

    def __init__(self, message: _Optional[str] = ...) -> None: ...
