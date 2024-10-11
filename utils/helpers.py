import qrcode
from io import BytesIO


async def create_qr(text: str) -> bytes:
    """Create a QR code from the given text and return it as bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create the QR image with custom colors
    qr_img = qr.make_image(fill_color="black", back_color="transparent").convert("RGBA")

    # Convert the image to bytes
    img_bytes_io = BytesIO()
    qr_img.save(img_bytes_io, "PNG")
    return img_bytes_io.getvalue()
