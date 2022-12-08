from gi.repository import GLib, GdkPixbuf  # type: ignore
from PIL import Image, ImageFont


def pixbuf2image(pix: GdkPixbuf.Pixbuf) -> Image.Image:
    """Convert gdkpixbuf to PIL image"""
    data = pix.get_pixels()
    w = pix.props.width
    h = pix.props.height
    stride = pix.props.rowstride
    mode = "RGB"
    if pix.props.has_alpha:
        mode = "RGBA"
    im = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
    return im


def image2pixbuf(im: Image.Image) -> GdkPixbuf.Pixbuf:
    """Convert Pillow image to GdkPixbuf"""
    data = im.tobytes()
    w, h = im.size
    data = GLib.Bytes.new(data)

    bands = im.getbands()
    has_alpha = "A" in bands
    rowstride = len(bands) * im.width
    pix = GdkPixbuf.Pixbuf.new_from_bytes(
        data, GdkPixbuf.Colorspace.RGB, has_alpha, 8, w, h, rowstride
    )
    return pix


def bound(source_width, source_height, bound_width, bound_height):
    """fits rect Source in rect Bound"""
    width_ratio = bound_width / source_width
    height_ratio = bound_height / source_height
    min_ratio = min(width_ratio, height_ratio)

    return int(source_width * min_ratio), int(source_height * min_ratio)


def calc_font_size(text, fontname, iw, ih):
    test_size = 100
    font = ImageFont.truetype(fontname, test_size)

    # get size
    l, t, r, b = font.getbbox(text)
    cur_width = r - l
    cur_height = b - t

    realsize_ratio = test_size / cur_height
    _, realsize_h = bound(cur_width, cur_height, iw, ih)

    return int(realsize_h * realsize_ratio)
