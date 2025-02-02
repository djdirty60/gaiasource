"""
Parser of FastTrackerII Extended Module (XM) version 1.4

Documents:
- Modplug source code (file modplug/soundlib/Load_mod.cpp)
  http://sourceforge.net/projects/modplug
- Dumb source code (files include/dumb.h and src/it/readmod.c
  http://dumb.sf.net/
- Documents on "MOD" format on Wotsit
  http://www.wotsit.org

Compressed formats (i.e. starting with "PP20" or having "PACK" as type
are not handled. Also NoiseTracker's NST modules aren't handled, although
it might be possible: no file format and 15 samples

Author: Christophe GISQUET <christophe.gisquet@free.fr>
Creation: 18th February 2007
"""

from math import log10
from externals.hachoir.parser import Parser
from externals.hachoir.field import (FieldSet,
                           Bits, UInt16, UInt8,
                           RawBytes, String, GenericVector)
from externals.hachoir.core.endian import BIG_ENDIAN
from externals.hachoir.core.text_handler import textHandler

# Old NoiseTracker 15-samples modules can have anything here.
MODULE_TYPE = {
    b"M.K.": ("Noise/Pro-Tracker", 4),
    b"M!K!": ("Noise/Pro-Tracker", 4),
    b"M&K&": ("Noise/Pro-Tracker", 4),
    b"RASP": ("StarTrekker", 4),
    b"FLT4": ("StarTrekker", 4),
    b"FLT8": ("StarTrekker", 8),
    b"6CHN": ("FastTracker", 6),
    b"8CHN": ("FastTracker", 8),
    b"CD81": ("Octalyser", 8),
    b"OCTA": ("Octalyser", 8),
    b"FA04": ("Digital Tracker", 4),
    b"FA06": ("Digital Tracker", 6),
    b"FA08": ("Digital Tracker", 8),
}


def getFineTune(val):
    return ("0", "1", "2", "3", "4", "5", "6", "7", "8",
            "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1")[val.value]


def getVolume(val):
    return "%.1f dB" % (20.0 * log10(val.value / 64.0))


class SampleInfo(FieldSet):
    static_size = 30 * 8

    def createFields(self):
        yield String(self, "name", 22, strip='\0')
        yield UInt16(self, "sample_count")
        yield textHandler(UInt8(self, "fine_tune"), getFineTune)
        yield textHandler(UInt8(self, "volume"), getVolume)
        yield UInt16(self, "loop_start", "Loop start offset in samples")
        yield UInt16(self, "loop_len", "Loop length in samples")

    def createValue(self):
        return self["name"].value


class Header(FieldSet):
    static_size = 1084 * 8

    def createFields(self):
        yield String(self, "name", 20, strip='\0')
        yield GenericVector(self, "samples", 31, SampleInfo, "info")
        yield UInt8(self, "length")
        yield UInt8(self, "played_patterns_count")
        yield GenericVector(self, "patterns", 128, UInt8, "position")
        yield String(self, "type", 4)

    def getNumChannels(self):
        return MODULE_TYPE[self["type"].value][1]


class Note(FieldSet):
    static_size = 8 * 4

    def createFields(self):
        yield Bits(self, 4, "note_hi_nibble")
        yield Bits(self, 12, "period")
        yield Bits(self, 4, "note_low_nibble")
        yield Bits(self, 4, "effect")
        yield UInt8(self, "parameter")


class Row(FieldSet):

    def __init__(self, parent, name, channels, desc=None):
        FieldSet.__init__(self, parent, name, description=desc)
        self.channels = channels
        self._size = 8 * self.channels * 4

    def createFields(self):
        for index in range(self.channels):
            yield Note(self, "note[]")


class Pattern(FieldSet):

    def __init__(self, parent, name, channels, desc=None):
        FieldSet.__init__(self, parent, name, description=desc)
        self.channels = channels
        self._size = 64 * 8 * self.channels * 4

    def createFields(self):
        for index in range(64):
            yield Row(self, "row[]", self.channels)


class AmigaModule(Parser):
    PARSER_TAGS = {
        "id": "mod",
        "category": "audio",
        "file_ext": ("mod", "nst", "wow", "oct", "sd0"),
        "mime": ('audio/mod', 'audio/x-mod', 'audio/mod', 'audio/x-mod'),
        "min_size": 1084 * 8,
        "description": "Uncompressed amiga module"
    }
    endian = BIG_ENDIAN

    def validate(self):
        modtype = self.stream.readBytes(1080 * 8, 4)
        if modtype not in MODULE_TYPE:
            return "Invalid module type %a" % modtype
        self.createValue = lambda modtype: "%s module, %u channels" % MODULE_TYPE[
            modtype]
        return True

    def createFields(self):
        header = Header(self, "header")
        yield header
        channels = header.getNumChannels()

        # Number of patterns
        patterns = 0
        for index in range(128):
            patterns = max(patterns,
                           header["patterns/position[%u]" % index].value)
        patterns += 1

        # Yield patterns
        for index in range(patterns):
            yield Pattern(self, "pattern[]", channels)

        # Yield samples
        for index in range(31):
            count = header["samples/info[%u]/sample_count" % index].value
            if count:
                self.info("Yielding sample %u: %u samples" % (index, count))
                yield RawBytes(self, "sample_data[]", 2 * count,
                               "Sample %u" % index)
