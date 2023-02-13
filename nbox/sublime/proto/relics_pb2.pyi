"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Relic(google.protobuf.message.Message):
    """Some terms and glossary for sanity:
    Relic: Relic is a folder on the cloud like a router which links to different files.
        A relic is the tree-group of individual files.
    RelicFile: RelicFile is a file in a relic which points to the correct location of the
        file on the cloud. Since this is not an object store in itself and only a pointer,
        different clients are responsible for figuring out how to download/uplaod the
        files.

    the main outer thing responsible for grouping files together
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    CREATED_ON_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_FIELD_NUMBER: builtins.int
    STARRED_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    WORKSPACE_ID_FIELD_NUMBER: builtins.int
    PERMISSION_FIELD_NUMBER: builtins.int
    UI_FIELD_FIELD_NUMBER: builtins.int
    BUCKET_META_FIELD_NUMBER: builtins.int
    id: typing.Text
    """these are the primary fields"""

    name: typing.Text
    created_on: builtins.int
    last_modified: builtins.int
    starred: builtins.bool
    """this is the starred functionality in NBX-Relics"""

    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """tags are like labels in NBX-Relics"""
        pass
    workspace_id: typing.Text
    @property
    def permission(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    @property
    def ui_field(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    @property
    def bucket_meta(self) -> global___BucketMetadata:
        """there are other things that may not be needed by the FE, think of this as the 
        NOTE: these are high index values so they can be expanded in the 1xx range
        a world with 100 clouds supported, would love to see that day.
        this can potentially become the metadata of the relic
        """
        pass
    def __init__(self,
        *,
        id: typing.Text = ...,
        name: typing.Text = ...,
        created_on: builtins.int = ...,
        last_modified: builtins.int = ...,
        starred: builtins.bool = ...,
        tags: typing.Optional[typing.Iterable[typing.Text]] = ...,
        workspace_id: typing.Text = ...,
        permission: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ui_field: typing.Optional[typing.Iterable[typing.Text]] = ...,
        bucket_meta: typing.Optional[global___BucketMetadata] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bucket_meta",b"bucket_meta"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bucket_meta",b"bucket_meta","created_on",b"created_on","id",b"id","last_modified",b"last_modified","name",b"name","permission",b"permission","starred",b"starred","tags",b"tags","ui_field",b"ui_field","workspace_id",b"workspace_id"]) -> None: ...
global___Relic = Relic

class BucketMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _Backend:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _BackendEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[BucketMetadata._Backend.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNSET: BucketMetadata._Backend.ValueType  # 0
        """leave it to NBX to figure out the backend"""

        AWS_S3: BucketMetadata._Backend.ValueType  # 1
        GCP_GCS: BucketMetadata._Backend.ValueType  # 2
        AZURE_BLOB: BucketMetadata._Backend.ValueType  # 3
        OCI_OB: BucketMetadata._Backend.ValueType  # 4
        DO_SPACES: BucketMetadata._Backend.ValueType  # 5
    class Backend(_Backend, metaclass=_BackendEnumTypeWrapper):
        pass

    UNSET: BucketMetadata.Backend.ValueType  # 0
    """leave it to NBX to figure out the backend"""

    AWS_S3: BucketMetadata.Backend.ValueType  # 1
    GCP_GCS: BucketMetadata.Backend.ValueType  # 2
    AZURE_BLOB: BucketMetadata.Backend.ValueType  # 3
    OCI_OB: BucketMetadata.Backend.ValueType  # 4
    DO_SPACES: BucketMetadata.Backend.ValueType  # 5

    class BucketTagsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    BUCKET_NAME_FIELD_NUMBER: builtins.int
    REGION_FIELD_NUMBER: builtins.int
    BACKEND_FIELD_NUMBER: builtins.int
    BUCKET_TAGS_FIELD_NUMBER: builtins.int
    bucket_name: typing.Text
    region: typing.Text
    backend: global___BucketMetadata.Backend.ValueType
    @property
    def bucket_tags(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]: ...
    def __init__(self,
        *,
        bucket_name: typing.Text = ...,
        region: typing.Text = ...,
        backend: global___BucketMetadata.Backend.ValueType = ...,
        bucket_tags: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["backend",b"backend","bucket_name",b"bucket_name","bucket_tags",b"bucket_tags","region",b"region"]) -> None: ...
global___BucketMetadata = BucketMetadata

class RelicFile(google.protobuf.message.Message):
    """RelicFile is like the individual object on the object store, at the end of
    the day an object store is nothing but a key value pair, where the "filepath"
    is the key and the "file" is the value. This basically means that "/" is
    ignored.
    Most of the fields are inspired from the macOS Finder.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _RelicType:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _RelicTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[RelicFile._RelicType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        FILE: RelicFile._RelicType.ValueType  # 0
        """file icon"""

        FOLDER: RelicFile._RelicType.ValueType  # 1
        """folder icon"""

        RELIC: RelicFile._RelicType.ValueType  # 2
        """potentially in the future we can symlink things"""

    class RelicType(_RelicType, metaclass=_RelicTypeEnumTypeWrapper):
        pass

    FILE: RelicFile.RelicType.ValueType  # 0
    """file icon"""

    FOLDER: RelicFile.RelicType.ValueType  # 1
    """folder icon"""

    RELIC: RelicFile.RelicType.ValueType  # 2
    """potentially in the future we can symlink things"""


    class HeadersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class BodyEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    NAME_FIELD_NUMBER: builtins.int
    CREATED_ON_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_FIELD_NUMBER: builtins.int
    STARRED_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    COMMENT_FIELD_NUMBER: builtins.int
    USERNAME_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    WORKSPACE_ID_FIELD_NUMBER: builtins.int
    RELIC_NAME_FIELD_NUMBER: builtins.int
    RELIC_ID_FIELD_NUMBER: builtins.int
    CONTENT_TYPE_FIELD_NUMBER: builtins.int
    DOWNLOAD_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    HEADERS_FIELD_NUMBER: builtins.int
    BODY_FIELD_NUMBER: builtins.int
    name: typing.Text
    created_on: builtins.int
    last_modified: builtins.int
    starred: builtins.bool
    """this is the starred functionality in NBX-Relics"""

    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """tags are like labels in NBX-Relics"""
        pass
    size: builtins.int
    """the size of the file"""

    comment: typing.Text
    """There are other "Human" aspects like comments, etc. This is all part of collaboration"""

    username: typing.Text
    """the creator of the file, this is a little bit ambivalent. Is this file created by the
    user or by the job. For now we are saying that this is the user who created the file.
    """

    type: global___RelicFile.RelicType.ValueType
    workspace_id: typing.Text
    relic_name: typing.Text
    """the name of the parent relic"""

    relic_id: typing.Text
    """the name of the parent relic"""

    content_type: typing.Text
    """Type of file content used to render the file in the browser"""

    download: builtins.bool
    """Used to set content disposition to the download file response."""

    url: typing.Text
    """NOTE: these are high index values so they can be expanded in the 1xx range
    this is all for the different clouds
    the url of the file
    """

    @property
    def headers(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """the headers to be used by the client"""
        pass
    @property
    def body(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """the body to be used by the client"""
        pass
    def __init__(self,
        *,
        name: typing.Text = ...,
        created_on: builtins.int = ...,
        last_modified: builtins.int = ...,
        starred: builtins.bool = ...,
        tags: typing.Optional[typing.Iterable[typing.Text]] = ...,
        size: builtins.int = ...,
        comment: typing.Text = ...,
        username: typing.Text = ...,
        type: global___RelicFile.RelicType.ValueType = ...,
        workspace_id: typing.Text = ...,
        relic_name: typing.Text = ...,
        relic_id: typing.Text = ...,
        content_type: typing.Text = ...,
        download: builtins.bool = ...,
        url: typing.Text = ...,
        headers: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        body: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["body",b"body","comment",b"comment","content_type",b"content_type","created_on",b"created_on","download",b"download","headers",b"headers","last_modified",b"last_modified","name",b"name","relic_id",b"relic_id","relic_name",b"relic_name","size",b"size","starred",b"starred","tags",b"tags","type",b"type","url",b"url","username",b"username","workspace_id",b"workspace_id"]) -> None: ...
global___RelicFile = RelicFile
