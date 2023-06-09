# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graphql.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="graphql.proto",
    package="dfuse.graphql.v1",
    syntax="proto3",
    serialized_options=b"Z8github.com/streamingfast/pbgo/dfuse/graphql/v1;pbgraphql",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\rgraphql.proto\x12\x10\x64\x66use.graphql.v1\x1a\x1cgoogle/protobuf/struct.proto"[\n\x07Request\x12\r\n\x05query\x18\x01 \x01(\t\x12*\n\tvariables\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x15\n\roperationName\x18\x03 \x01(\t"A\n\x08Response\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12\'\n\x06\x65rrors\x18\x02 \x03(\x0b\x32\x17.dfuse.graphql.v1.Error"\xa4\x01\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x33\n\tlocations\x18\x02 \x03(\x0b\x32 .dfuse.graphql.v1.SourceLocation\x12(\n\x04path\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12+\n\nextensions\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct".\n\x0eSourceLocation\x12\x0c\n\x04line\x18\x01 \x01(\x05\x12\x0e\n\x06\x63olumn\x18\x02 \x01(\x05"=\n\x0b\x42lockCursor\x12\x0b\n\x03ver\x18\x01 \x01(\x05\x12\x10\n\x08\x62lockNum\x18\x02 \x01(\x04\x12\x0f\n\x07\x62lockId\x18\x03 \x01(\t"S\n\x11TransactionCursor\x12\x0b\n\x03ver\x18\x01 \x01(\x05\x12\x18\n\x10transactionIndex\x18\x02 \x01(\r\x12\x17\n\x0ftransactionHash\x18\x03 \x01(\t2O\n\x07GraphQL\x12\x44\n\x07\x45xecute\x12\x19.dfuse.graphql.v1.Request\x1a\x1a.dfuse.graphql.v1.Response"\x00\x30\x01\x42:Z8github.com/streamingfast/pbgo/dfuse/graphql/v1;pbgraphqlb\x06proto3',
    dependencies=[
        google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,
    ],
)


_REQUEST = _descriptor.Descriptor(
    name="Request",
    full_name="dfuse.graphql.v1.Request",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="query",
            full_name="dfuse.graphql.v1.Request.query",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="variables",
            full_name="dfuse.graphql.v1.Request.variables",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="operationName",
            full_name="dfuse.graphql.v1.Request.operationName",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=65,
    serialized_end=156,
)


_RESPONSE = _descriptor.Descriptor(
    name="Response",
    full_name="dfuse.graphql.v1.Response",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="data",
            full_name="dfuse.graphql.v1.Response.data",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="errors",
            full_name="dfuse.graphql.v1.Response.errors",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=158,
    serialized_end=223,
)


_ERROR = _descriptor.Descriptor(
    name="Error",
    full_name="dfuse.graphql.v1.Error",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="message",
            full_name="dfuse.graphql.v1.Error.message",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="locations",
            full_name="dfuse.graphql.v1.Error.locations",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="path",
            full_name="dfuse.graphql.v1.Error.path",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="extensions",
            full_name="dfuse.graphql.v1.Error.extensions",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=226,
    serialized_end=390,
)


_SOURCELOCATION = _descriptor.Descriptor(
    name="SourceLocation",
    full_name="dfuse.graphql.v1.SourceLocation",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="line",
            full_name="dfuse.graphql.v1.SourceLocation.line",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="column",
            full_name="dfuse.graphql.v1.SourceLocation.column",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=392,
    serialized_end=438,
)


_BLOCKCURSOR = _descriptor.Descriptor(
    name="BlockCursor",
    full_name="dfuse.graphql.v1.BlockCursor",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="ver",
            full_name="dfuse.graphql.v1.BlockCursor.ver",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="blockNum",
            full_name="dfuse.graphql.v1.BlockCursor.blockNum",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="blockId",
            full_name="dfuse.graphql.v1.BlockCursor.blockId",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=440,
    serialized_end=501,
)


_TRANSACTIONCURSOR = _descriptor.Descriptor(
    name="TransactionCursor",
    full_name="dfuse.graphql.v1.TransactionCursor",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="ver",
            full_name="dfuse.graphql.v1.TransactionCursor.ver",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="transactionIndex",
            full_name="dfuse.graphql.v1.TransactionCursor.transactionIndex",
            index=1,
            number=2,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="transactionHash",
            full_name="dfuse.graphql.v1.TransactionCursor.transactionHash",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=503,
    serialized_end=586,
)

_REQUEST.fields_by_name[
    "variables"
].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_RESPONSE.fields_by_name["errors"].message_type = _ERROR
_ERROR.fields_by_name["locations"].message_type = _SOURCELOCATION
_ERROR.fields_by_name[
    "path"
].message_type = google_dot_protobuf_dot_struct__pb2._LISTVALUE
_ERROR.fields_by_name[
    "extensions"
].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name["Request"] = _REQUEST
DESCRIPTOR.message_types_by_name["Response"] = _RESPONSE
DESCRIPTOR.message_types_by_name["Error"] = _ERROR
DESCRIPTOR.message_types_by_name["SourceLocation"] = _SOURCELOCATION
DESCRIPTOR.message_types_by_name["BlockCursor"] = _BLOCKCURSOR
DESCRIPTOR.message_types_by_name["TransactionCursor"] = _TRANSACTIONCURSOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType(
    "Request",
    (_message.Message,),
    {
        "DESCRIPTOR": _REQUEST,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.Request)
    },
)
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType(
    "Response",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESPONSE,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.Response)
    },
)
_sym_db.RegisterMessage(Response)

Error = _reflection.GeneratedProtocolMessageType(
    "Error",
    (_message.Message,),
    {
        "DESCRIPTOR": _ERROR,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.Error)
    },
)
_sym_db.RegisterMessage(Error)

SourceLocation = _reflection.GeneratedProtocolMessageType(
    "SourceLocation",
    (_message.Message,),
    {
        "DESCRIPTOR": _SOURCELOCATION,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.SourceLocation)
    },
)
_sym_db.RegisterMessage(SourceLocation)

BlockCursor = _reflection.GeneratedProtocolMessageType(
    "BlockCursor",
    (_message.Message,),
    {
        "DESCRIPTOR": _BLOCKCURSOR,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.BlockCursor)
    },
)
_sym_db.RegisterMessage(BlockCursor)

TransactionCursor = _reflection.GeneratedProtocolMessageType(
    "TransactionCursor",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSACTIONCURSOR,
        "__module__": "graphql_pb2"
        # @@protoc_insertion_point(class_scope:dfuse.graphql.v1.TransactionCursor)
    },
)
_sym_db.RegisterMessage(TransactionCursor)


DESCRIPTOR._options = None

_GRAPHQL = _descriptor.ServiceDescriptor(
    name="GraphQL",
    full_name="dfuse.graphql.v1.GraphQL",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=588,
    serialized_end=667,
    methods=[
        _descriptor.MethodDescriptor(
            name="Execute",
            full_name="dfuse.graphql.v1.GraphQL.Execute",
            index=0,
            containing_service=None,
            input_type=_REQUEST,
            output_type=_RESPONSE,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_GRAPHQL)

DESCRIPTOR.services_by_name["GraphQL"] = _GRAPHQL

# @@protoc_insertion_point(module_scope)
