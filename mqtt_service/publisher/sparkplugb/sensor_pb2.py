# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: sensor.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'sensor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csensor.proto\x12\x06sensor\"\"\n\rSensorRequest\x12\x11\n\tdevice_id\x18\x01 \x01(\t\"\xae\x02\n\x0eSensorResponse\x12\x11\n\tdevice_id\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65vice_name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x18\n\x10last_maintenance\x18\x05 \x01(\t\x12\x1c\n\x14next_maintenance_due\x18\x06 \x01(\t\x12\x13\n\x0btemperature\x18\x07 \x01(\x02\x12\x18\n\x10temperature_unit\x18\x08 \x01(\t\x12\x10\n\x08humidity\x18\t \x01(\x02\x12\x15\n\rhumidity_unit\x18\n \x01(\t\x12\x0c\n\x04site\x18\x0b \x01(\t\x12\x0c\n\x04room\x18\x0c \x01(\t\x12\x10\n\x08latitude\x18\r \x01(\x02\x12\x11\n\tlongitude\x18\x0e \x01(\x02\x32O\n\rSensorService\x12>\n\rGetSensorData\x12\x15.sensor.SensorRequest\x1a\x16.sensor.SensorResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sensor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SENSORREQUEST']._serialized_start=24
  _globals['_SENSORREQUEST']._serialized_end=58
  _globals['_SENSORRESPONSE']._serialized_start=61
  _globals['_SENSORRESPONSE']._serialized_end=363
  _globals['_SENSORSERVICE']._serialized_start=365
  _globals['_SENSORSERVICE']._serialized_end=444
# @@protoc_insertion_point(module_scope)
