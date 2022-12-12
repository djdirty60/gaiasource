# Field classes
from externals.hachoir.field.field import Field, FieldError, MissingField, joinPath  # noqa
from externals.hachoir.field.bit_field import Bit, Bits, RawBits  # noqa
from externals.hachoir.field.byte_field import Bytes, RawBytes  # noqa
from externals.hachoir.field.sub_file import SubFile, CompressedField  # noqa
from externals.hachoir.field.character import Character  # noqa
from externals.hachoir.field.integer import (Int8,  Int16,  Int24,  Int32,  Int64,  # noqa
                                   UInt8, UInt16, UInt24, UInt32, UInt64,
                                   GenericInteger)
from externals.hachoir.field.enum import Enum  # noqa
from externals.hachoir.field.string_field import (GenericString,  # noqa
                                        String, CString, UnixLine,
                                        PascalString8, PascalString16,
                                        PascalString32)
from externals.hachoir.field.padding import (PaddingBits, PaddingBytes,  # noqa
                                   NullBits, NullBytes)

# Functions
from externals.hachoir.field.helper import (isString, isInteger,  # noqa
                                  createPaddingField, createNullField,
                                  createRawField, writeIntoFile,
                                  createOrphanField)

# FieldSet classes
from externals.hachoir.field.fake_array import FakeArray  # noqa
from externals.hachoir.field.basic_field_set import (BasicFieldSet,  # noqa
                                           ParserError, MatchError)
from externals.hachoir.field.generic_field_set import GenericFieldSet  # noqa
from externals.hachoir.field.seekable_field_set import SeekableFieldSet, RootSeekableFieldSet  # noqa
from externals.hachoir.field.field_set import FieldSet  # noqa
from externals.hachoir.field.static_field_set import StaticFieldSet  # noqa
from externals.hachoir.field.parser import Parser  # noqa
from externals.hachoir.field.vector import GenericVector, UserVector  # noqa

# Complex types
from externals.hachoir.field.float import Float32, Float64, Float80  # noqa
from externals.hachoir.field.timestamp import (  # noqa
    GenericTimestamp,
    TimestampUnix32, TimestampUnix64, TimestampMac32, TimestampUUID60,
    TimestampWin64, TimedeltaMillisWin64,
    DateTimeMSDOS32, TimeDateMSDOS32, TimedeltaWin64)

# Special Field classes
from externals.hachoir.field.link import Link, Fragment  # noqa
from externals.hachoir.field.fragment import FragmentGroup, CustomFragment  # noqa

available_types = (Bit, Bits, RawBits,
                   Bytes, RawBytes,
                   SubFile,
                   Character,
                   Int8, Int16, Int24, Int32, Int64,
                   UInt8, UInt16, UInt24, UInt32, UInt64,
                   String, CString, UnixLine,
                   PascalString8, PascalString16, PascalString32,
                   Float32, Float64,
                   PaddingBits, PaddingBytes,
                   NullBits, NullBytes,
                   TimestampUnix32, TimestampMac32, TimestampWin64,
                   TimedeltaMillisWin64,
                   DateTimeMSDOS32, TimeDateMSDOS32,
                   #                   GenericInteger, GenericString,
                   )
