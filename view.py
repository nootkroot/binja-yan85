import struct

from binaryninja import (Architecture, BinaryView, Endianness,
                         SectionSemantics, SegmentFlag)


class Yan85Loader(BinaryView):
    name = "yan85"
    long_name = "yan85 loader"

    def __init__(self, data):
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
        self.raw = data

    @classmethod
    def is_valid_for_data(cls, data):
        return data.read(0, 8) == b"yan85\x00\x00\x00"

    def perform_get_default_endianness(self):
        return Endianness.BigEndian

    def init(self):
        self.platform = Architecture["yan85"].standalone_platform
        self.arch = Architecture["yan85"]

        code_len = struct.unpack("<I", self.raw[8:12])[0]

        self.add_auto_segment(
            0x0,
            0x300,
            12,
            code_len,
            SegmentFlag.SegmentReadable
            | SegmentFlag.SegmentContainsCode
            | SegmentFlag.SegmentExecutable,
        )
        self.add_auto_section(
            ".code", 0x0, 0x300, SectionSemantics.ReadOnlyCodeSectionSemantics
        )

        self.add_auto_segment(
            0x300,
            0x100,
            code_len + 12,
            0x100,
            SegmentFlag.SegmentReadable
            | SegmentFlag.SegmentContainsData
            | SegmentFlag.SegmentWritable,
        )
        self.add_auto_section(
            ".data", 0x300, 0x100, SectionSemantics.ReadWriteDataSectionSemantics
        )
        return True

    def perform_is_executable(self):
        return True

    def perform_get_entry_point(self):
        return 0

    def perform_get_address_size(self):
        return self.arch.address_size
