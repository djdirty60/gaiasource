# -*- coding: utf-8 -*-
from externals.pymaging.colors import RGBA
from externals.pymaging.png.raw import Writer

def write(image, fileobj):
    writer = Writer(
        width=image.width,
        height=image.height,
        alpha=image.mode is RGBA,
        palette=image.palette,
    )
    writer.write_array(fileobj, image.pixels.data)
