import os
import qrcode
from functools import lru_cache
from io import BytesIO
from PIL import Image
from ..config import env


@lru_cache(maxsize=1)
def get_processed_background(background_path):
    """Cache the background image with minimal processing"""
    if not background_path or not os.path.exists(background_path):
        return None

    try:
        with Image.open(background_path) as img:
            if img.size[0] > 1000 or img.size[1] > 1000:
                img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            return img.convert("RGBA")
    except (IOError, OSError):
        return None


async def create_qr(text: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    backphoto = env.QR_BACKGROUND
    background = get_processed_background(backphoto) if backphoto else None

    if background is None:
        img_bytes_io = BytesIO()
        qr_img.save(img_bytes_io, "PNG", optimize=True, quality=95)
        return img_bytes_io.getvalue()

    new_size = tuple(int(0.6 * min(background.size)) for _ in range(2))
    qr_img_resized = qr_img.resize(new_size, Image.Resampling.LANCZOS)

    position = (
        (background.size[0] - new_size[0]) // 2,
        (background.size[1] - new_size[1]) // 2,
    )

    final_img = background.copy()
    white_bg = Image.new("RGBA", new_size, (255, 255, 255, 255))
    final_img.paste(white_bg, position, white_bg)
    final_img.paste(qr_img_resized, position, qr_img_resized)

    img_bytes_io = BytesIO()
    final_img.save(
        img_bytes_io,
        "PNG",
        optimize=True,
        quality=95,
        compress_level=6,
    )

    return img_bytes_io.getvalue()
