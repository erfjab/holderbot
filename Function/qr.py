from io import BytesIO
import qrcode

def DEF_CREATE_QRCODE(MESSAGE_TEXT) :
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    qr.add_data(MESSAGE_TEXT)
    qr.make(fit=True)
    # if you want change qr color , you need change "fill_color"
    qr_img = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    qr_img.save(img_bytes_io, 'PNG')
    img_bytes_io.seek(0)
    return img_bytes_io
