# for image IO
from PIL import Image

# for DCT (cv2 works fine)
from cv2 import dct, idct
from math import cos, sqrt, pi

# for bit insertion
from statistics import median

from parameters import *
import numpy as np

# def local_dct(P):
#     C = np.zeros((8, 8))
#     for row in range(8):
#         for column in range(8):
#             if row == 0:
#                 C[row][column] = 1 / sqrt(8)
#             else:
#                 C[row][column] = (1 / 2) * cos((2 * column + 1) * row * pi / 16)
#     return np.matmul(np.matmul(C, P), C.T)

# def local_idct(G):
#     C = np.zeros((8, 8))
#     for row in range(8):
#         for column in range(8):
#             if row == 0:
#                 C[row][column] = 1 / sqrt(8)
#             else:
#                 C[row][column] = (1 / 2) * cos((2 * column + 1) * row * pi / 16)
#     return np.matmul(np.matmul(C.T, G), C)

def local_dct(array):
    return dct(np.float32(array))

def local_idct(array):
    return idct(np.float32(array))

def init(container_path):
    global g, ROW, COLUMN
    container = Image.open(container_path)
    width, height = container.size
    container_map = np.zeros((width, height, 3))
    for row in range(height):
        for column in range(width):
            r, gr, b = container.getpixel((row, column))
            container_map[row, column] = np.array([r, gr, b])
    # print(container_map)
    g.container_map = container_map
    g.width = width
    g.height = height
    g.filename = container_path

def insert_block(matrix, bit, next_matrix):
    global g
    # print('initial: ')
    # print(matrix)
    # m = matrix.copy()
    matrix = local_dct(matrix)
    next_matrix = local_dct(next_matrix)
    # next_matrix = np.zeros((8, 8))
    # print('changed: ')
    # print(np.round(local_idct(matrix), 0) == m)
    # print('dct')
    # print(matrix)
    AC_9 = sorted([matrix[0, 1], matrix[0, 2], matrix[0, 3], \
                   matrix[1, 1], matrix[1, 2], matrix[2, 1], \
                   matrix[1, 0], matrix[2, 0], matrix[3, 0]])
    DC = matrix[0, 0]
    M = None
    med = median(AC_9)
    if abs(DC) > 1000 or abs(DC) < 1:
        M = abs(g.Z * med)
    else:
        M = abs(g.Z * (DC - med) / DC)
    delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
    if bit:
        if delta > (g.T - g.K):
            while delta > (g.T - g.K):
                matrix[g.row, g.column] = matrix[g.row, g.column] - M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
        elif g.K > delta > (-g.T // 2):
            while delta < g.K:
                matrix[g.row, g.column] = matrix[g.row, g.column] + M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
                # print(delta, M, matrix[g.row, g.column])
        elif delta < (-g.T // 2):
            while delta > (-g.T - g.K):
                matrix[g.row, g.column] = matrix[g.row, g.column] - M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
    else:
        if delta > (g.T // 2):
            while delta <= (g.T + g.K):
                matrix[g.row, g.column] = matrix[g.row, g.column] + M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
        elif (-g.K) < delta < (g.T // 2):
            while delta >= (-g.K):
                matrix[g.row, g.column] = matrix[g.row, g.column] - M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
        elif delta < (g.K - g.T):
            while delta <= (g.K - g.T):
                matrix[g.row, g.column] = matrix[g.row, g.column] + M
                delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
    # print('result (dct): ')
    # print(matrix)
    # print('result (inverted): ')
    # print(local_idct(matrix))
    return local_idct(matrix)

def extract_block(matrix, next_matrix):
    global g
    # next_matrix = np.subtract(next_matrix, 128)
    # print('matrix decoded: ')
    # print(matrix)
    matrix = local_dct(matrix)
    next_matrix = local_dct(next_matrix)
    # next_matrix = np.zeros((8, 8))
    delta = matrix[g.row, g.column] - next_matrix[g.row, g.column]
    w = None
    if delta < (-g.T) or ((delta > 0) and (delta < g.T)):
        w = 1
    else:
        w = 0
    # print('dct: ')
    # print(matrix)
    # print(w)
    return w

def arnold_transformation(binary_matrix, times):
    size = len(binary_matrix)
    new_binary_matrix = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            coordinates = np.array([[row], [column]])
            default = np.array([[1, 1], [1, 2]])
            for _ in range(times):
                coordinates = np.matmul(default, coordinates)
            new_binary_matrix[coordinates[0][0] % size][coordinates[1][0] % size] = binary_matrix[row][column]

    return np.array(new_binary_matrix)

def inverse_arnold_transformation(binary_matrix, times):
    size = len(binary_matrix)
    new_binary_matrix = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            coordinates = np.array([[row], [column]])
            default = np.array([[2, -1], [-1, 1]])
            for _ in range(times):
                coordinates = np.matmul(default, coordinates)
            new_binary_matrix[coordinates[0][0] % size][coordinates[1][0] % size] = binary_matrix[row][column]

    return np.array(new_binary_matrix)

def insert(watermark_map):
    global g
    container_map = g.container_map
    watermark_map = arnold_transformation(watermark_map, 1)
    # watermark_map = watermark_map
    # watermark_map = np.zeros((8, 8))
    blue = np.subtract(container_map[:, :, 2], 128)
    for brs in range(0, g.height, 8):
        for bcs in range(0, g.width, 8):
            block = blue[brs:brs + 8, bcs:bcs + 8]
            next_block = blue[brs:brs + 8, \
                             bcs + 8:bcs + 16]
            if bcs + 8 == g.width:
                next_block = blue[brs:brs + 8, 0:8]
            # next_block = np.zeros((8, 8))
            bit = watermark_map[brs // 8, bcs // 8]
            # print(block, next_block, sep='\n')
            # print(bcs, brs)
            g.row = g.row + (bcs // 8) % 2
            g.column = g.column + (bcs // 8) % 2
            new_block = insert_block(block, bit, next_block)
            g.row = g.row - (bcs // 8) % 2
            g.column = g.column - (bcs // 8) % 2
            # print(f'start of block: {bcs}, end: {brs}, bit: {bit}')
            # print('initial block: ')
            # print(np.round(block))
            # print('changed block: ')
            # print(np.round(new_block))
            # print(f'target value: {block[g.row, g.column]}')
            # print(f'target value (changed): {block[g.row, g.column]}')
            blue[brs:brs + 8, bcs:bcs + 8] = new_block
    for row in range(g.height):
        for column in range(g.width):
            R, G, B = container_map[row, column]
            # print(R, G, B)
            B = int(blue[row, column]) + 128
            # B = round(new_copy[row, column], 0)
            # print(B)
            container_map[row, column] = np.array([R, G, B])
    g.container_map = container_map

def extract():
    global g
    container_map = g.container_map
    watermark_map = np.zeros((container_map.shape[0] // 8, \
                              container_map.shape[0] // 8))
    blue = np.subtract(container_map[:, :, 2], 128)
    for brs in range(0, g.height, 8):
        for bcs in range(0, g.width, 8):
            block = blue[brs:brs + 8, bcs:bcs + 8]
            # print(block)
            next_block = blue[brs:brs + 8, \
                             bcs + 8:bcs + 16]
            if bcs + 8 == g.width:
                next_block = blue[brs:brs + 8, 0:8]
            # next_block = np.zeros((8, 8))
            # print(block, next_block, brs, bcs)
            g.row = g.row + (bcs // 8) % 2
            g.column = g.column + (bcs // 8) % 2
            bit = extract_block(block, next_block)
            g.row = g.row - (bcs // 8) % 2
            g.column = g.column - (bcs // 8) % 2
            watermark_map[brs // 8, bcs // 8] = bit

    # print(watermark_map)
    return inverse_arnold_transformation(watermark_map, 1)
    # return watermark_map
            

def finalize(output_path):
    global g
    img = Image.open(g.filename)
    matrix = img.load()
    for row in range(g.width):
        for column in range(g.height):
            matrix[row, column] = tuple(g.container_map[row, column].astype(int))
    
    img.save(output_path)


    


