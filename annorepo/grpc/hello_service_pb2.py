# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hello_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13hello_service.proto\x12\x1cnl.knaw.huc.annorepo.grpc.v1\"0\n\x0fSayHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x61pi_key\x18\x02 \x01(\t\"#\n\x10SayHelloResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2y\n\x0cHelloService\x12i\n\x08SayHello\x12-.nl.knaw.huc.annorepo.grpc.v1.SayHelloRequest\x1a..nl.knaw.huc.annorepo.grpc.v1.SayHelloResponseB0\n\x19nl.knaw.huc.annorepo.grpcB\x11HelloServiceProtoP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hello_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\031nl.knaw.huc.annorepo.grpcB\021HelloServiceProtoP\001'
    _globals['_SAYHELLOREQUEST']._serialized_start = 53
    _globals['_SAYHELLOREQUEST']._serialized_end = 101
    _globals['_SAYHELLORESPONSE']._serialized_start = 103
    _globals['_SAYHELLORESPONSE']._serialized_end = 138
    _globals['_HELLOSERVICE']._serialized_start = 140
    _globals['_HELLOSERVICE']._serialized_end = 261
# @@protoc_insertion_point(module_scope)
