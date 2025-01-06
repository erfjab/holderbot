import qrcode
from functools import lru_cache
from io import BytesIO
from PIL import Image
from ..config import env


@lru_cache(maxsize=1)
def get_processed_background(background_path):
    """Cache the background image with minimal processing"""
    if not background_path:
        return None

    with Image.open(background_path) as img:
        return img.convert("RGB")


async def create_qr(text: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("L")

    backphoto = env.QR_BACKGROUND
    if backphoto:
        background = get_processed_background(backphoto)
        if background is None:
            img_bytes_io = BytesIO()
            qr_img.save(img_bytes_io, "JPEG", quality=50)
            return img_bytes_io.getvalue()

        new_size = (background.size[0] // 2, background.size[1] // 2)
        qr_img_resized = qr_img.resize(new_size, Image.NEAREST)

        position = (
            (background.size[0] - new_size[0]) >> 1,
            (background.size[1] - new_size[1]) >> 1,
        )

        final_img = background.copy()

        white_bg = Image.new("L", new_size, 255)
        final_img.paste(white_bg, position)
        final_img.paste(qr_img_resized, position)

    else:
        final_img = qr_img

    img_bytes_io = BytesIO()
    final_img.save(img_bytes_io, "JPEG", quality=50, optimize=False, progressive=False)

    return img_bytes_io.getvalue()
