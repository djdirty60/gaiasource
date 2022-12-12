from externals.pymaging import Image
from externals.pymaging.colors import RGB
from externals.pymaging.formats import registry
from externals.pymaging.shapes import Line
from externals.pymaging.webcolors import Black, White
from externals.pymaging.png.png import PNG

import externals.qrcode.image.base


class PymagingImage(externals.qrcode.image.base.BaseImage):
    """
    pymaging image builder, default format is PNG.
    """
    kind = "PNG"
    allowed_kinds = ("PNG",)

    def __init__(self, *args, **kwargs):
        """
        Register PNG with pymaging.
        """
        registry.formats = []
        registry.names = {}
        registry._populate()
        registry.register(PNG)

        super().__init__(*args, **kwargs)

    def new_image(self, **kwargs):
        # GAIACODE
        #return Image.new(RGB, self.pixel_size, self.pixel_size, White)
        from externals.pymaging.colors import Color, RGBA
        self.back_color = kwargs.get("back_color", "white")
        self.back_color = Color(red = self.back_color[0], green = self.back_color[1], blue = self.back_color[2], alpha = self.back_color[3])
        self.fill_color = kwargs.get("fill_color", "black")
        self.fill_color = Color(red = self.fill_color[0], green = self.fill_color[1], blue = self.fill_color[2], alpha = self.fill_color[3])
        return Image.new(RGBA, self.pixel_size, self.pixel_size, self.back_color)

    def drawrect(self, row, col):
        (x, y), (x2, y2) = self.pixel_box(row, col)
        for r in range(self.box_size):
            line_y = y + r
            line = Line(x, line_y, x2, line_y)
            # GAIACODE
            #self._img.draw(line, Black)
            self._img.draw(line, self.fill_color)

    def save(self, stream, kind=None):
        # GAIACODE
        #self._img.save(stream, self.check_kind(kind))
        if isinstance(stream, str): self._img.save_to_path(stream, self.check_kind(kind))
        else: self._img.save(stream, self.check_kind(kind))

    def check_kind(self, kind, transform=None, **kwargs):
        """
        pymaging (pymaging_png at least) uses lower case for the type.
        """
        if transform is None:
            transform = lambda x: x.lower()
        return super().check_kind(
            kind, transform=transform, **kwargs)
