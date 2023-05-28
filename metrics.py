from PIL import Image
from math import sqrt, log10
from insertion import extract, init

def check_mse(img_src, img_out):
    img_src = Image.open(img_src)
    img_out = Image.open(img_out)
    pixels_src = list(img_src.getdata())
    pixels_out = list(img_out.getdata())
    height, width = img_out.size
    mse = 0
    for i in range(height * width):
        red_1, green_1, blue_1 = pixels_src[i]
        red_2, green_2, blue_2 = pixels_out[i]
        mse += (blue_1 - blue_2) ** 2
    return mse * (1 / (height * width))

def check_psnr(img_src, img_out):
    mse = check_mse(img_src, img_out)
    return 10 * log10(255 ** 2 / mse)

def check_rmse(img_src, img_out):
    mse = check_mse(img_src, img_out)
    return sqrt(mse)

def check_ber(img_init, img_out):
    img_out = Image.open(img_out)
    pixels_out = list(img_out.getdata())
    img_init = Image.open(img_init)
    pixels_init = list(img_init.getdata())
    height, width = img_init.size
    errors = 0
    for i in range(height * width):
        errors += pixels_out[i] != pixels_init[i]
    return errors / (height * width)
