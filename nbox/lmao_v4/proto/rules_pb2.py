# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rules.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0brules.proto\x12\x07lmao_pb\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9f\x01\n\x05Logic\x12\x13\n\x0b\x61\x63tion_type\x18\x01 \x01(\t\x12,\n\x0b\x61\x63tion_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12&\n\x05\x65xtra\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\njson_logic\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"m\n\x0fInitRuleRequest\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x12\n\nproject_id\x18\x02 \x01(\t\x12\x11\n\trule_name\x18\x04 \x01(\t\x12\x1d\n\x05logic\x18\x07 \x01(\x0b\x32\x0e.lmao_pb.Logic\"\xfb\x01\n\x04Rule\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x12\n\nproject_id\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x11\n\trule_name\x18\x04 \x01(\t\x12.\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x0eis_deactivated\x18\x07 \x01(\x08\x12\x1d\n\x05logic\x18\x08 \x01(\x0b\x32\x0e.lmao_pb.Logic\x12\x13\n\x0bupdate_keys\x18\t \x03(\t\"S\n\tRulesList\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x12\n\nproject_id\x18\x02 \x01(\t\x12\x1c\n\x05rules\x18\x03 \x03(\x0b\x32\r.lmao_pb.Rule\"V\n\x0bRuleBuilder\x12\x14\n\x0cworkspace_id\x18\x01 \x01(\t\x12\x12\n\nproject_id\x18\x02 \x01(\t\x12\x1d\n\x05logic\x18\x03 \x01(\x0b\x32\x0e.lmao_pb.LogicB/Z-github.com/NimbleBoxAI/nimblebox-lmao/lmao_pbb\x06proto3')



_LOGIC = DESCRIPTOR.message_types_by_name['Logic']
_INITRULEREQUEST = DESCRIPTOR.message_types_by_name['InitRuleRequest']
_RULE = DESCRIPTOR.message_types_by_name['Rule']
_RULESLIST = DESCRIPTOR.message_types_by_name['RulesList']
_RULEBUILDER = DESCRIPTOR.message_types_by_name['RuleBuilder']
Logic = _reflection.GeneratedProtocolMessageType('Logic', (_message.Message,), {
  'DESCRIPTOR' : _LOGIC,
  '__module__' : 'rules_pb2'
  # @@protoc_insertion_point(class_scope:lmao_pb.Logic)
  })
_sym_db.RegisterMessage(Logic)

InitRuleRequest = _reflection.GeneratedProtocolMessageType('InitRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITRULEREQUEST,
  '__module__' : 'rules_pb2'
  # @@protoc_insertion_point(class_scope:lmao_pb.InitRuleRequest)
  })
_sym_db.RegisterMessage(InitRuleRequest)

Rule = _reflection.GeneratedProtocolMessageType('Rule', (_message.Message,), {
  'DESCRIPTOR' : _RULE,
  '__module__' : 'rules_pb2'
  # @@protoc_insertion_point(class_scope:lmao_pb.Rule)
  })
_sym_db.RegisterMessage(Rule)

RulesList = _reflection.GeneratedProtocolMessageType('RulesList', (_message.Message,), {
  'DESCRIPTOR' : _RULESLIST,
  '__module__' : 'rules_pb2'
  # @@protoc_insertion_point(class_scope:lmao_pb.RulesList)
  })
_sym_db.RegisterMessage(RulesList)

RuleBuilder = _reflection.GeneratedProtocolMessageType('RuleBuilder', (_message.Message,), {
  'DESCRIPTOR' : _RULEBUILDER,
  '__module__' : 'rules_pb2'
  # @@protoc_insertion_point(class_scope:lmao_pb.RuleBuilder)
  })
_sym_db.RegisterMessage(RuleBuilder)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/NimbleBoxAI/nimblebox-lmao/lmao_pb'
  _LOGIC._serialized_start=88
  _LOGIC._serialized_end=247
  _INITRULEREQUEST._serialized_start=249
  _INITRULEREQUEST._serialized_end=358
  _RULE._serialized_start=361
  _RULE._serialized_end=612
  _RULESLIST._serialized_start=614
  _RULESLIST._serialized_end=697
  _RULEBUILDER._serialized_start=699
  _RULEBUILDER._serialized_end=785
# @@protoc_insertion_point(module_scope)
