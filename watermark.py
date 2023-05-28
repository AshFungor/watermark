from PIL import Image
import numpy as np


def decode_8b(path):

    img = Image.open(path).convert('L')
    width, height = img.size
    matrix = np.zeros((width, height))
    for row in range(height):
        for column in range(width):
            grey = img.getpixel((row, column))
            matrix[row, column] = grey

    binary = np.zeros((height * 8, width * 8))
    for row in range(height):
        for column in range(0, width * 8, 8):
            pixel_bin = bin(int(matrix[row, column // 8]))[2:]
            pixel_bin = '0' * (8 - len(pixel_bin)) + pixel_bin
            bit_array = np.array(list(map(lambda bit: int(bit), pixel_bin)))
            for i in range(column, column + 8):
                binary[row][i] = bit_array[i % 8]

    return width, height, binary

def encode_8b(binary, width, height, path):
    img = Image.new(mode="L", size=(height, width))
    matrix = img.load()
    for row in range(height):
        for column in range(0, width * 8, 8):
            bits = []
            for i in range(column, column + 8):
                bits.append(str(int(binary[row, i])))
            pixel = int(''.join(bits), 2)
            matrix[row, column // 8] = pixel
    img.save(path)

def convert_g1(path, new_path):
    img = Image.open(path).convert('L')
    width, height = img.size
    matrix = np.zeros((width, height))
    for row in range(height):
        for column in range(width):
            grey = img.getpixel((row, column))
            matrix[row, column] = grey

    new_img = Image.new(mode="L", size=(height, width))
    binary = new_img.load()

    for row in range(height):
        for column in range(width):
            pixel_bin = 1 if matrix[row, column] > 127 else 0
            binary[row, column] = 255 if pixel_bin else 0

    new_img.save(new_path)

def decode_1b(path):
    img = Image.open(path).convert('L')
    width, height = img.size
    matrix = np.zeros((width, height))
    for row in range(height):
        for column in range(width):
            grey = img.getpixel((row, column))
            matrix[row, column] = grey

    binary = np.zeros((height, width))
    for row in range(height):
        for column in range(width):
            pixel_bin = 1 if matrix[row, column] > 127 else 0
            binary[row, column] = pixel_bin

    return width, height, binary

def encode_1b(binary, width, height, path):
    img = Image.new(mode="L", size=(height, width))
    matrix = img.load()
    for row in range(height):
        for column in range(width):
            pixel = 255 if binary[row, column] else 0
            matrix[row, column] = int(pixel)
    img.save(path)

    
    
