import qrcode
from io import BytesIO
from PIL import Image
from ..config import env


async def create_qr(text: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    backphoto = env.QR_BACKGROUND
    if backphoto:
        background = Image.open(backphoto).convert("RGBA")

        max_size = (800, 800)
        if background.size[0] > max_size[0] or background.size[1] > max_size[1]:
            background.thumbnail(max_size, Image.LANCZOS)

        new_size = tuple(int(0.65 * min(background.size)) for _ in range(2))
        qr_img_resized = qr_img.resize(new_size, Image.LANCZOS)

        position = tuple((background.size[i] - new_size[i]) // 2 for i in range(2))

        white_background = Image.new("RGBA", qr_img_resized.size, (255, 255, 255, 255))

        final_img = Image.new("RGBA", background.size, (0, 0, 0, 0))
        final_img.paste(background, (0, 0))

        final_img.paste(white_background, position, white_background)
        final_img.paste(qr_img_resized, position, qr_img_resized)
    else:
        final_img = qr_img

    img_bytes_io = BytesIO()

    final_img.save(
        img_bytes_io,
        "PNG",
        optimize=True,
        quality=60,
    )
    return img_bytes_io.getvalue()
