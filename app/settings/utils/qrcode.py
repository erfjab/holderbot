from io import BytesIO
import qrcode


async def create_qr(text: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="transparent").convert("RGBA")
    img_bytes_io = BytesIO()
    qr_img.save(img_bytes_io, "PNG")
    return img_bytes_io.getvalue()
