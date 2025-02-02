from externals.hachoir.metadata.metadata import RootMetadata, registerExtractor
from externals.hachoir.metadata.image import computeComprRate
from externals.hachoir.parser.image.exif import IFD, BasicIFDEntry
from externals.hachoir.parser.image.jpeg import (
    JpegFile, JpegChunk,
    QUALITY_HASH_COLOR, QUALITY_SUM_COLOR,
    QUALITY_HASH_GRAY, QUALITY_SUM_GRAY)
from externals.hachoir.field import MissingField
from externals.hachoir.core.tools import makeUnicode
from externals.hachoir.metadata.safe import fault_tolerant
from datetime import datetime


def deg2float(degree, minute, second):
    return degree + (float(minute) + float(second) / 60.0) / 60.0


class JpegMetadata(RootMetadata):
    EXIF_KEY = {
        # Exif metadatas
        "Make": "camera_manufacturer",
        "Model": "camera_model",
        "Orientation": "image_orientation",
        "ExposureTime": "camera_exposure",
        "FNumber": "camera_focal",
        "BrightnessValue": "camera_brightness",
        "MaxApertureValue": "camera_aperture",
        "ISOSpeedRatings": "iso_speed_ratings",
        "ExifVersion": "exif_version",
        "DateTimeOriginal": "date_time_original",
        "DateTimeDigitized": "date_time_digitized",
        "CompressedBitsPerPixel": "compressed_bits_per_pixel",
        "ShutterSpeedValue": "shutter_speed_value",
        "ApertureValue": "aperture_value",
        "ExposureBiasValue": "exposure_bias_value",
        "FocalLength": "focal_length",
        "FlashpixVersion": "flashpix_version",
        "FocalPlaneXResolution": "focal_plane_x_resolution",
        "FocalPlaneYResolution": "focal_plane_y_resolution",
        "FocalLengthIn35mmFilm": "focal_length_in_35mm_film",

        # Generic metadatas
        "ImageDescription": "title",
        "Software": "producer",
        "DateTime": "creation_date",
        "PixelXDimension": "width",
        "PixelYDimension": "height",
        "UserComment": "comment",
        "JPEGInterchangeFormatLength": "thumbnail_size",
    }

    IPTC_KEY = {
        80: "author",
        90: "city",
        101: "country",
        116: "copyright",
        120: "title",
        231: "comment",
    }

    orientation_name = {
        1: 'Horizontal (normal)',
        2: 'Mirrored horizontal',
        3: 'Rotated 180',
        4: 'Mirrored vertical',
        5: 'Mirrored horizontal then rotated 90 counter-clock-wise',
        6: 'Rotated 90 clock-wise',
        7: 'Mirrored horizontal then rotated 90 clock-wise',
        8: 'Rotated 90 counter clock-wise',
    }

    def extract(self, jpeg):
        if "start_frame/content" in jpeg:
            self.startOfFrame(jpeg["start_frame/content"])
        elif "start_scan/content/nr_components" in jpeg:
            self.bits_per_pixel = 8 * \
                jpeg["start_scan/content/nr_components"].value
        if "app0/content" in jpeg:
            self.extractAPP0(jpeg["app0/content"])

        if "exif/content" in jpeg:
            for ifd in jpeg['exif/content']:
                if not isinstance(ifd, IFD):
                    continue
                for entry in ifd.array("entry"):
                    self.processIfdEntry(ifd, entry)
                self.readGPS(ifd)
        if "photoshop/content" in jpeg:
            psd = jpeg["photoshop/content"]
            if "version/content/reader_name" in psd:
                self.producer = psd["version/content/reader_name"].value
            if "iptc/content" in psd:
                self.parseIPTC(psd["iptc/content"])
        for field in jpeg.array("comment"):
            if "content/comment" in field:
                self.comment = field["content/comment"].value
        self.computeQuality(jpeg)
        if "data" in jpeg:
            computeComprRate(self, jpeg["data"].size)
        if not self.has("producer") and "photoshop" in jpeg:
            self.producer = "Adobe Photoshop"
        if self.has("compression"):
            self.compression = "JPEG"

    @fault_tolerant
    def startOfFrame(self, sof):
        # Set compression method
        key = sof["../type"].value
        self.compression = "JPEG (%s)" % JpegChunk.START_OF_FRAME[key]

        # Read image size and bits/pixel
        self.width = sof["width"].value
        self.height = sof["height"].value
        nb_components = sof["nr_components"].value
        self.bits_per_pixel = 8 * nb_components
        if nb_components == 3:
            self.pixel_format = "YCbCr"
        elif nb_components == 1:
            self.pixel_format = "Grayscale"
            self.nb_colors = 256

    @fault_tolerant
    def computeQuality(self, jpeg):
        # This function is an adaption to Python of ImageMagick code
        # to compute JPEG quality using quantization tables

        # Read quantization tables
        qtlist = []
        for dqt in jpeg.array("quantization"):
            for qt in dqt.array("content/qt"):
                # TODO: Take care of qt["index"].value?
                qtlist.append(qt)
        if not qtlist:
            return

        # Compute sum of all coefficients
        sumcoeff = 0
        for qt in qtlist:
            coeff = qt.array("coeff")
            for index in range(64):
                sumcoeff += coeff[index].value

        # Choose the right quality table and compute hash value
        try:
            hashval = qtlist[0]["coeff[2]"].value + \
                qtlist[0]["coeff[53]"].value
            if 2 <= len(qtlist):
                hashval += qtlist[1]["coeff[0]"].value + \
                    qtlist[1]["coeff[63]"].value
                hashtable = QUALITY_HASH_COLOR
                sumtable = QUALITY_SUM_COLOR
            else:
                hashtable = QUALITY_HASH_GRAY
                sumtable = QUALITY_SUM_GRAY
        except (MissingField, IndexError):
            # A coefficient is missing, so don't compute JPEG quality
            return

        # Find the JPEG quality
        for index in range(100):
            if (hashval >= hashtable[index]) or (sumcoeff >= sumtable[index]):
                quality = "%s%%" % (index + 1)
                if (hashval > hashtable[index]) or (sumcoeff > sumtable[index]):
                    quality += " " + "(approximate)"
                self.comment = "JPEG quality: %s" % quality
                return

    @fault_tolerant
    def extractAPP0(self, app0):
        self.format_version = "JFIF %u.%02u" \
            % (app0["ver_maj"].value, app0["ver_min"].value)
        if "y_density" in app0:
            self.width_dpi = app0["x_density"].value
            self.height_dpi = app0["y_density"].value

    @fault_tolerant
    def processIfdEntry(self, ifd, entry):
        # Skip unknown tags
        tag = entry["tag"].display
        if tag not in self.EXIF_KEY:
            return
        key = self.EXIF_KEY[tag]
        if key in ("width", "height") and self.has(key):
            # EXIF "valid size" are sometimes not updated when the image is scaled
            # so we just ignore it
            return

        # Read value
        value = ifd.getEntryValues(entry)[0].value

        # Convert value to string
        if tag == "Orientation":
            value = self.orientation_name.get(value, value)
        elif tag == "ExposureTime":
            if not value:
                return
            if isinstance(value, float):
                value = (value, "1/%g" % (1 / value))
        elif entry["type"].value in (BasicIFDEntry.TYPE_RATIONAL, BasicIFDEntry.TYPE_SIGNED_RATIONAL):
            value = (value, "%.3g" % value)

        # Store information
        setattr(self, key, value)

    @fault_tolerant
    def readGPS(self, ifd):
        # Read latitude and longitude
        latitude_ref = None
        longitude_ref = None
        latitude = None
        longitude = None
        altitude_ref = 1
        altitude = None
        timestamp = None
        datestamp = None
        for entry in ifd.array("entry"):
            tag = entry["tag"].display
            values = [v.value for v in ifd.getEntryValues(entry)]
            if tag == "GPSLatitudeRef":
                if values[0] == "N":
                    latitude_ref = 1
                else:
                    latitude_ref = -1
            elif tag == "GPSLongitudeRef":
                if values[0] == "E":
                    longitude_ref = 1
                else:
                    longitude_ref = -1
            elif tag == "GPSAltitudeRef":
                if values[0] == 1:
                    altitude_ref = -1
                else:
                    altitude_ref = 1
            elif tag == "GPSLatitude":
                latitude = values
            elif tag == "GPSLongitude":
                longitude = values
            elif tag == "GPSAltitude":
                altitude = values[0]
            elif tag == "GPSDateStamp":
                datestamp = values[0]
            elif tag == "GPSTimeStamp":
                timestamp = ':'.join(str(int(x)) for x in values)
        if latitude_ref and latitude:
            value = deg2float(*latitude)
            if latitude_ref < 0:
                value = -value
            self.latitude = value
        if longitude and longitude_ref:
            value = deg2float(*longitude)
            if longitude_ref < 0:
                value = -value
            self.longitude = value
        if altitude:
            value = altitude
            if altitude_ref < 0:
                value = -value
            self.altitude = value
        if datestamp:
            if timestamp:
                datestamp += " " + timestamp
            self.creation_date = datestamp

    def parseIPTC(self, iptc):
        datestr = hourstr = None
        for field in iptc:
            # Skip incomplete field
            if "tag" not in field or "content" not in field:
                continue

            # Get value
            value = field["content"].value
            if isinstance(value, str):
                value = value.replace("\r", " ")
                value = value.replace("\n", " ")

            # Skip unknown tag
            tag = field["tag"].value
            if tag == 55:
                datestr = value
                continue
            if tag == 60:
                hourstr = value
                continue
            if tag not in self.IPTC_KEY:
                if tag != 0:
                    self.warning("Skip IPTC key %s: %s" % (
                        field["tag"].display, makeUnicode(value)))
                continue
            setattr(self, self.IPTC_KEY[tag], value)
        if datestr and hourstr:
            try:
                year = int(datestr[0:4])
                month = int(datestr[4:6])
                day = int(datestr[6:8])
                hour = int(hourstr[0:2])
                min = int(hourstr[2:4])
                sec = int(hourstr[4:6])
                self.creation_date = datetime(year, month, day, hour, min, sec)
            except ValueError:
                pass


registerExtractor(JpegFile, JpegMetadata)
