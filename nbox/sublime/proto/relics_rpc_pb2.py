# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/relics_rpc.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nbox.sublime.proto import relics_pb2 as proto_dot_relics__pb2
from nbox.sublime.proto import common_pb2 as proto_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16proto/relics_rpc.proto\x1a\x12proto/relics.proto\x1a\x12proto/common.proto\"\xa6\x01\n\x12\x43reateRelicRequest\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06region\x18\x03 \x01(\t\x12\x1d\n\x15nbx_integration_token\x18\x04 \x01(\t\x12\x17\n\x0fnbx_resource_id\x18\x05 \x01(\t\x12$\n\x0b\x62ucket_meta\x18\x06 \x01(\x0b\x32\x0f.BucketMetadata\"`\n\x11ListRelicsRequest\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x12\n\nrelic_name\x18\x02 \x01(\t\x12\x0f\n\x07page_no\x18\x03 \x01(\x05\x12\x10\n\x08relic_id\x18\x04 \x01(\t\"B\n\x12ListRelicsResponse\x12\x16\n\x06relics\x18\x01 \x03(\x0b\x32\x06.Relic\x12\x14\n\x0ctotal_relics\x18\x02 \x01(\x05\"\x87\x01\n\x15ListRelicFilesRequest\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x10\n\x08relic_id\x18\x02 \x01(\t\x12\x12\n\nrelic_name\x18\x03 \x01(\t\x12\x0e\n\x06prefix\x18\x04 \x01(\t\x12\x11\n\tfile_name\x18\x05 \x01(\t\x12\x0f\n\x07page_no\x18\x06 \x01(\x05\"H\n\x16ListRelicFilesResponse\x12\x19\n\x05\x66iles\x18\x01 \x03(\x0b\x32\n.RelicFile\x12\x13\n\x0btotal_files\x18\x02 \x01(\x05\"\x93\x01\n\x12\x41\x63tivityLogRequest\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x10\n\x08relic_id\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x19\n\x11\x66rom_timestamp_ns\x18\x04 \x01(\x03\x12\x17\n\x0fto_timestamp_ns\x18\x05 \x01(\x03\x12\x0f\n\x07page_no\x18\x06 \x01(\x05\"y\n\x0b\x41\x63tivityLog\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x03\x12\x10\n\x08relic_id\x18\x02 \x01(\t\x12\x1b\n\toperation\x18\x03 \x01(\x0e\x32\x08.Actions\x12\x13\n\x0bobject_size\x18\x04 \x01(\x02\x12\x10\n\x08username\x18\x05 \x01(\t\"1\n\x13\x41\x63tivityLogResponse\x12\x1a\n\x04logs\x18\x01 \x03(\x0b\x32\x0c.ActivityLog*7\n\x07\x41\x63tions\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06\x43REATE\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06\x44\x45LETE\x10\x03\x32\xfe\x03\n\nRelicStore\x12-\n\x0c\x63reate_relic\x12\x13.CreateRelicRequest\x1a\x06.Relic\"\x00\x12\x38\n\x0blist_relics\x12\x12.ListRelicsRequest\x1a\x13.ListRelicsResponse\"\x00\x12+\n\x11update_relic_meta\x12\x06.Relic\x1a\x0c.Acknowledge\"\x00\x12&\n\x0c\x64\x65lete_relic\x12\x06.Relic\x1a\x0c.Acknowledge\"\x00\x12%\n\x11get_relic_details\x12\x06.Relic\x1a\x06.Relic\"\x00\x12\'\n\x0b\x63reate_file\x12\n.RelicFile\x1a\n.RelicFile\"\x00\x12\x45\n\x10list_relic_files\x12\x16.ListRelicFilesRequest\x1a\x17.ListRelicFilesResponse\"\x00\x12/\n\x11\x64\x65lete_relic_file\x12\n.RelicFile\x1a\x0c.Acknowledge\"\x00\x12)\n\rdownload_file\x12\n.RelicFile\x1a\n.RelicFile\"\x00\x12?\n\x10get_activity_log\x12\x13.ActivityLogRequest\x1a\x14.ActivityLogResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.relics_rpc_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACTIONS._serialized_start=937
  _ACTIONS._serialized_end=992
  _CREATERELICREQUEST._serialized_start=67
  _CREATERELICREQUEST._serialized_end=233
  _LISTRELICSREQUEST._serialized_start=235
  _LISTRELICSREQUEST._serialized_end=331
  _LISTRELICSRESPONSE._serialized_start=333
  _LISTRELICSRESPONSE._serialized_end=399
  _LISTRELICFILESREQUEST._serialized_start=402
  _LISTRELICFILESREQUEST._serialized_end=537
  _LISTRELICFILESRESPONSE._serialized_start=539
  _LISTRELICFILESRESPONSE._serialized_end=611
  _ACTIVITYLOGREQUEST._serialized_start=614
  _ACTIVITYLOGREQUEST._serialized_end=761
  _ACTIVITYLOG._serialized_start=763
  _ACTIVITYLOG._serialized_end=884
  _ACTIVITYLOGRESPONSE._serialized_start=886
  _ACTIVITYLOGRESPONSE._serialized_end=935
  _RELICSTORE._serialized_start=995
  _RELICSTORE._serialized_end=1505
# @@protoc_insertion_point(module_scope)
