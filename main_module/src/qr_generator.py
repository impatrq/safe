import qrcode
from PIL import Image
import json
import os

FILE_DIR = os.path.dirname(__file__) + "/"

def generate(mac):
    logo_link = FILE_DIR + f"images/qr_img/logo.jpg"
  
    logo = Image.open(logo_link)
    
    # taking base width
    basewidth = 400
    
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=2,
        box_size=25
    )
    
    # taking url or text
    data_dict = {"mac": mac, "sanitizer": "100%"}
    data = json.dumps(data_dict)
    # addingg URL or text to QRcode
    QRcode.add_data(data)
    
    # generating QR code
    QRcode.make()
    
    # taking color name from user
    QRcolor = 'Black'
    
    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')
    
    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    
    # save the QR code generated
    QRimg.save( FILE_DIR + f"images/qr_img/qr_safe.png")
    
    print('QR code generated!')
    return FILE_DIR + f"images/qr_img/qr_safe.png"
