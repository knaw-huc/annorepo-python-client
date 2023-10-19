from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, \
    Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor


class AddAnnotationsRequest(_message.Message):
    __slots__ = ["api_key", "container_name", "annotation"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    container_name: str
    annotation: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, api_key: _Optional[str] = ..., container_name: _Optional[str] = ...,
                 annotation: _Optional[_Iterable[str]] = ...) -> None: ...


class AnnotationIdentifier(_message.Message):
    __slots__ = ["id", "etag"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    id: str
    etag: str

    def __init__(self, id: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...


class AddAnnotationsResponse(_message.Message):
    __slots__ = ["annotation_identifier"]
    ANNOTATION_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    annotation_identifier: _containers.RepeatedCompositeFieldContainer[AnnotationIdentifier]

    def __init__(self,
                 annotation_identifier: _Optional[_Iterable[_Union[AnnotationIdentifier, _Mapping]]] = ...) -> None: ...


class NamedAnnotation(_message.Message):
    __slots__ = ["preferred_name", "annotation"]
    PREFERRED_NAME_FIELD_NUMBER: _ClassVar[int]
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    preferred_name: str
    annotation: str

    def __init__(self, preferred_name: _Optional[str] = ..., annotation: _Optional[str] = ...) -> None: ...
