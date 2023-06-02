from insertion import *
from watermark import *
from metrics import *
from parameters import g

from PIL import Image, ImageFilter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

result_folder = 'results'
container_folder = 'containers'
watermark_folder = 'watermarks'

def test_routine():
    global g
    psnr_s = []
    ber_blur = []
    ber_sharpen = []
    ber_smooth = []
    ber_jpeg1 = []
    ber_jpeg2 = []
    table_1 = open(f'{result_folder}/psnr_data.txt', 'w')
    table_2 = open(f'{result_folder}/avg_ber_data.txt', 'w')
    for column in range(0, 7, 2):
        for row in range(0, 8, 2):
            if column == 0 and row == 0:
                continue
            g.row = row
            g.column = column
            psnr, ber_s = base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
            psnr_s.append(psnr)
            ber_blur.append(ber_s[0])
            ber_sharpen.append(ber_s[1])
            ber_smooth.append(ber_s[2])
            ber_jpeg1.append(ber_s[3])
            ber_jpeg2.append(ber_s[4])
            table_1.write(f'{round(psnr, 3)}\t')
            table_2.write(f'{round(sum(ber_s) / len(ber_s), 3)}\t')
        table_1.write('\n')
        table_2.write('\n')
        r = range(0, 8, 2)
        if column == 0:
            r = list(range(0, 8, 2))
            r.remove(0)
        plt.plot(r, ber_blur, color='Orange')
        plt.xticks(r)
        plt.plot(r, ber_sharpen, color='Blue')
        plt.xticks(r)
        plt.plot(r, ber_smooth, color='Red')
        plt.xticks(r)
        plt.plot(r, ber_jpeg1, color='Green')
        plt.xticks(r)
        plt.plot(r, ber_jpeg2, color='Purple')
        plt.xticks(r)
        plt.xlabel(f'row, for column = {column}')
        plt.ylabel('BER')
        plt.legend(['blur', 'sharpen', 'smooth', 'jpeg (1)', 'jpeg (2)'])
        # plt.show()
        plt.savefig(f'{result_folder}/ber_plot_{row}_{column}.png')
        plt.clf()
        ber_blur.clear()
        ber_sharpen.clear()
        ber_smooth.clear()
        ber_jpeg1.clear()
        ber_jpeg2.clear()
        plt.plot(r, psnr_s, color='Blue')
        plt.xticks(r)
        plt.xlabel(f'row, for column = {column}')
        plt.ylabel('PSNR')
        # plt.show()
        plt.savefig(f'{result_folder}/psnr_plot_{row}_{column}.png')
        plt.clf()
        psnr_s.clear()
    table_2.close()
    table_1.close()

def coefficient_test_k():
    global g
    results = open(f'{result_folder}/psnr_and_ber_coefficients_data.txt', 'w')
    psnr_s = []
    ber_blur = []
    ber_sharpen = []
    ber_smooth = []
    ber_jpeg1 = []
    ber_jpeg2 = []
    for k in range(12, 100, 12):
        g.K = k
        psnr, ber_s = base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
        results.write(f'Z = {g.Z}; K = {g.K}; T = {g.T}; PSNR = {round(psnr, 3)}; AVG_BER = {round(sum(ber_s) / len(ber_s), 3)}\n')
        psnr_s.append(psnr)
        ber_blur.append(ber_s[0])
        ber_sharpen.append(ber_s[1])
        ber_smooth.append(ber_s[2])
        ber_jpeg1.append(ber_s[3])
        ber_jpeg2.append(ber_s[4])
    r = range(12, 100, 12)
    plt.plot(r, ber_blur, color='Orange')
    plt.xticks(r)
    plt.plot(r, ber_sharpen, color='Blue')
    plt.xticks(r)
    plt.plot(r, ber_smooth, color='Red')
    plt.xticks(r)
    plt.plot(r, ber_jpeg1, color='Green')
    plt.xticks(r)
    plt.plot(r, ber_jpeg2, color='Purple')
    plt.xticks(r)
    plt.xlabel(f'K')
    plt.ylabel('BER')
    plt.legend(['blur', 'sharpen', 'smooth', 'jpeg (1)', 'jpeg (2)'])
    # plt.show()
    plt.savefig(f'{result_folder}/ber_plot_ber_k.png')
    plt.clf()
    ber_blur.clear()
    ber_sharpen.clear()
    ber_smooth.clear()
    ber_jpeg1.clear()
    ber_jpeg2.clear()
    plt.plot(r, psnr_s, color='Blue')
    plt.xticks(r)
    plt.xlabel(f'K')
    plt.ylabel('PSNR')
    plt.savefig(f'{result_folder}/psnr_plot_psnr_k.png')
    plt.clf()
    results.close()

def coefficient_test_t():
    global g
    results = open(f'{result_folder}/psnr_and_ber_coefficients_data.txt', 'w')
    psnr_s = []
    ber_blur = []
    ber_sharpen = []
    ber_smooth = []
    ber_jpeg1 = []
    ber_jpeg2 = []
    for t in range(80, 500, 30):
        g.T = t
        g.K = int(t * 0.15)
        psnr, ber_s = base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
        results.write(f'Z = {g.Z}; K = {g.K}; T = {g.T}; PSNR = {round(psnr, 3)}; AVG_BER = {round(sum(ber_s) / len(ber_s), 3)}\n')
        psnr_s.append(psnr)
        ber_blur.append(ber_s[0])
        ber_sharpen.append(ber_s[1])
        ber_smooth.append(ber_s[2])
        ber_jpeg1.append(ber_s[3])
        ber_jpeg2.append(ber_s[4])
    r = range(80, 500, 30)
    plt.plot(r, ber_blur, color='Orange')
    plt.xticks(r)
    plt.plot(r, ber_sharpen, color='Blue')
    plt.xticks(r)
    plt.plot(r, ber_smooth, color='Red')
    plt.xticks(r)
    plt.plot(r, ber_jpeg1, color='Green')
    plt.xticks(r)
    plt.plot(r, ber_jpeg2, color='Purple')
    plt.xticks(r)
    plt.xlabel(f'T')
    plt.ylabel('BER')
    plt.legend(['blur', 'sharpen', 'smooth', 'jpeg (1)', 'jpeg (2)'])
    # plt.show()
    plt.savefig(f'{result_folder}/ber_plot_ber_t.png')
    plt.clf()
    ber_blur.clear()
    ber_sharpen.clear()
    ber_smooth.clear()
    ber_jpeg1.clear()
    ber_jpeg2.clear()
    plt.plot(r, psnr_s, color='Blue')
    plt.xticks(r)
    plt.xlabel(f'T')
    plt.ylabel('PSNR')
    plt.savefig(f'{result_folder}/psnr_plot_psnr_t.png')
    plt.clf()
    results.close()

def coefficient_test_z():
    global g
    results = open(f'{result_folder}/psnr_and_ber_coefficients_data.txt', 'w')
    psnr_s = []
    ber_blur = []
    ber_sharpen = []
    ber_smooth = []
    ber_jpeg1 = []
    ber_jpeg2 = []
    for z in range(2, 50, 5):
        g.Z = z
        psnr, ber_s = base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
        results.write(f'Z = {g.Z}; K = {g.K}; T = {g.T}; PSNR = {round(psnr, 3)}; AVG_BER = {round(sum(ber_s) / len(ber_s), 3)}\n')
        psnr_s.append(psnr)
        ber_blur.append(ber_s[0])
        ber_sharpen.append(ber_s[1])
        ber_smooth.append(ber_s[2])
        ber_jpeg1.append(ber_s[3])
        ber_jpeg2.append(ber_s[4])
    r = range(2, 50, 5)
    plt.plot(r, ber_blur, color='Orange')
    plt.xticks(r)
    plt.plot(r, ber_sharpen, color='Blue')
    plt.xticks(r)
    plt.plot(r, ber_smooth, color='Red')
    plt.xticks(r)
    plt.plot(r, ber_jpeg1, color='Green')
    plt.xticks(r)
    plt.plot(r, ber_jpeg2, color='Purple')
    plt.xticks(r)
    plt.xlabel(f'Z')
    plt.ylabel('BER')
    plt.legend(['blur', 'sharpen', 'smooth', 'jpeg (1)', 'jpeg (2)'])
    # plt.show()
    plt.savefig(f'{result_folder}/ber_plot_ber_z.png')
    plt.clf()
    ber_blur.clear()
    ber_sharpen.clear()
    ber_smooth.clear()
    ber_jpeg1.clear()
    ber_jpeg2.clear()
    plt.plot(r, psnr_s, color='Blue')
    plt.xticks(r)
    plt.xlabel(f'Z')
    plt.ylabel('PSNR')
    plt.savefig(f'{result_folder}/psnr_plot_psnr_z.png')
    plt.clf()
    results.close()

def coefficients_test_ultimate():
    global g
    results = open(f'{result_folder}/psnr_and_ber_coefficients_data.txt', 'w')
    psnr_s = []
    ber_blur = []
    ber_sharpen = []
    ber_smooth = []
    ber_jpeg1 = []
    ber_jpeg2 = []
    for t in range(80, 500, 30):
        g.T = t
        g.K = int(t * 0.15)
        g.Z = int(g.K / 6)
        psnr, ber_s = base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
        results.write(f'Z = {g.Z}; K = {g.K}; T = {g.T}; PSNR = {round(psnr, 3)}; AVG_BER = {round(sum(ber_s) / len(ber_s), 3)}\n')
        psnr_s.append(psnr)
        ber_blur.append(ber_s[0])
        ber_sharpen.append(ber_s[1])
        ber_smooth.append(ber_s[2])
        ber_jpeg1.append(ber_s[3])
        ber_jpeg2.append(ber_s[4])
    r = range(80, 500, 30)
    plt.plot(r, ber_blur, color='Orange')
    plt.xticks(r)
    plt.plot(r, ber_sharpen, color='Blue')
    plt.xticks(r)
    plt.plot(r, ber_smooth, color='Red')
    plt.xticks(r)
    plt.plot(r, ber_jpeg1, color='Green')
    plt.xticks(r)
    plt.plot(r, ber_jpeg2, color='Purple')
    plt.xticks(r)
    plt.xlabel(f'T')
    plt.ylabel('BER')
    plt.legend(['blur', 'sharpen', 'smooth', 'jpeg (1)', 'jpeg (2)'])
    # plt.show()
    plt.savefig(f'{result_folder}/ber_plot_ber_all.png')
    plt.clf()
    ber_blur.clear()
    ber_sharpen.clear()
    ber_smooth.clear()
    ber_jpeg1.clear()
    ber_jpeg2.clear()
    plt.plot(r, psnr_s, color='Blue')
    plt.xticks(r)
    plt.xlabel(f'T')
    plt.ylabel('PSNR')
    plt.savefig(f'{result_folder}/psnr_plot_psnr_all.png')
    plt.clf()
    results.close()

def jpeg_test():
    ber_s = []
    init(f'{container_folder}/container_tank_cat.png')
    g.Z = 2
    g.K = 12
    g.T = 80
    for row, column in [(2, 2)]:
        g.row = row
        g.column = column
        print('Performing JPEG (0-100) test for:')
        print(f'Z: {g.Z}; T: {g.T}; K: {g.K}; ROW: {g.row}; COLUMN: {g.column}')
        convert_g1(f'{watermark_folder}/psi.png', f'{result_folder}/watermark_temp.png')
        w_width, w_height, mat = decode_1b(f'{result_folder}/watermark_temp.png')
        insert(mat)
        finalize(f'{result_folder}/result.png')
        for quality in range(0, 101, 5):
            print(f'testing JPEG ({quality})...')
            img = Image.open(f'{result_folder}/result.png')
            img.save(f'{result_folder}/jpeg_{quality}.jpeg', quality=quality)
            init(f'{result_folder}/jpeg_{quality}.jpeg')
            res = extract()
            encode_1b(res, w_width, w_height, f'{result_folder}/watermark_jpeg_{quality}.png')
            ber_s.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_jpeg_{quality}.png'))
        plt.plot(range(0, 101, 5), ber_s)
        plt.xlabel(f'quality')
        plt.ylabel('BER')
        plt.savefig(f'{result_folder}/ber_jpeg_{row}_{column}.png')
        ber_s.clear()
        plt.clf()


def base_test(container_path, watermark_path):
    global g
    # test for current global settings
    init(container_path)
    print('Performing tests for globals: ')
    print(f'Z: {g.Z}; T: {g.T}; K: {g.K}; ROW: {g.row}; COLUMN: {g.column}')
    print('Running insertion...')
    convert_g1(watermark_path, f'{result_folder}/watermark_temp.png')
    w_width, w_height, mat = decode_1b(f'{result_folder}/watermark_temp.png')
    insert(mat)
    finalize(f'{result_folder}/result.png')
    PSNR = check_psnr(container_path, f'{result_folder}/result.png')
    BER = list()
    # test (BLUR)
    print('testing BLUR...')
    img = Image.open(f'{result_folder}/result.png').filter(ImageFilter.BLUR)
    img.save(f'{result_folder}/result_blur.png')
    init(f'{result_folder}/result_blur.png')
    res = extract()
    encode_1b(res, w_width, w_height, f'{result_folder}/watermark_blur.png')
    BER.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_blur.png'))
    # test (SHARPEN)
    print('testing SHARPEN...')
    img = Image.open(f'{result_folder}/result.png').filter(ImageFilter.SHARPEN)
    img.save(f'{result_folder}/result_sharpen.png')
    init(f'{result_folder}/result_sharpen.png')
    res = extract()
    encode_1b(res, w_width, w_height, f'{result_folder}/watermark_sharpen.png')
    BER.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_sharpen.png'))
    # test (SMOOTH)
    print('testing SMOOTH...')
    img = Image.open(f'{result_folder}/result.png').filter(ImageFilter.SMOOTH)
    img.save(f'{result_folder}/result_smooth.png')
    init(f'{result_folder}/result_smooth.png')
    res = extract()
    encode_1b(res, w_width, w_height, f'{result_folder}/watermark_smooth.png')
    BER.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_smooth.png'))
    # test (JPEG) (1)
    print('testing JPEG (1)...')
    img = Image.open(f'{result_folder}/result.png')
    img.save(f'{result_folder}/jpeg_1.jpeg', quality=100)
    init(f'{result_folder}/jpeg_1.jpeg')
    res = extract()
    encode_1b(res, w_width, w_height, f'{result_folder}/watermark_jpeg_1.png')
    BER.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_jpeg_1.png'))
    # test (JPEG) (2)
    print('testing JPEG (2)...')
    img = Image.open(f'{result_folder}/jpeg_1.jpeg')
    img.save(f'{result_folder}/jpeg_2.jpeg', quality=100)
    init(f'{result_folder}/jpeg_2.jpeg')
    res = extract()
    encode_1b(res, w_width, w_height, f'{result_folder}/watermark_jpeg_2.png')
    BER.append(check_ber(f'{result_folder}/watermark_temp.png', f'{result_folder}/watermark_jpeg_2.png'))
    print('Statistics: ')
    print(f'PSNR:           {PSNR}')
    print(f'BER (BLUR):     {BER[0]}')
    print(f'BER (SHARPEN):  {BER[1]}')
    print(f'BER (SMOOTH):   {BER[2]}')
    print(f'BER (JPEG-1):   {BER[3]}')
    print(f'BER (JPEG-2):   {BER[4]}')
    return PSNR, BER



if __name__ == '__main__':
    print('Welcome to watermark insertion program. Would you like to run a routine? [Yes/No]')
    ans = input()
    if ans.lower() == 'y' or ans.lower() == 'yes':
        print('Which routine you would like to run?')
        print('1 - Coefficient location test')
        print('2 - JPEG test')
        print('3 - Base tests for defaults')
        print('4 - Coefficient test for K')
        print('5 - Coefficient test for T')
        print('6 - Coefficient test for Z')
        print('7 - Coefficient test for T, K and Z (proportional)')
        ans = input()
        if ans == '1':
            test_routine()
        elif ans == '2':
            jpeg_test()
        elif ans == '3':
            base_test(f'{container_folder}/container_tank_cat.png', f'{watermark_folder}/psi.png')
        elif ans == '4':
            coefficient_test_k()
        elif ans == '5':
            coefficient_test_t()
        elif ans == '6':
            coefficient_test_z()
        elif ans == '7':
            coefficients_test_ultimate()
        else:
            raise ValueError('expected inputs between 1-2')
    else:
        print('Switched to interactive mode!')
        ans = ''
        while ans.lower() != 'q' and ans.lower() != 'quit':
            print('What task do you need to perform?')
            print('[Insert] - insert the watermark into the container')
            print('[Extract] - extract the watermark from the container')
            print('[Quit] - quit this application')
            ans = input()
            if ans.lower() == 'i' or ans.lower() == 'insert':
                watermark = input('Type name of the watermark that you want to insert: ')
                container = input('Type name of the container, that should hold your watermark: ')
                init(f'{container_folder}/{container}')
                convert_g1(f'{watermark_folder}/{watermark}', f'{result_folder}/watermark_temp.png')
                w_width, w_height, mat = decode_1b(f'{result_folder}/watermark_temp.png')
                insert(mat)
                finalize(f'{result_folder}/result.png')
                print(f'Done! See your new container at {result_folder}/result.png')
            if ans.lower() == 'e' or ans.lower() == 'extract':
                container = input('Type name of the container, that holds watermark: ')
                init(f'{result_folder}/{container}')
                res = extract()
                encode_1b(res, w_width, w_height, f'{result_folder}/watermark_result.png')
                print(f'Done! See your watermark at {result_folder}/watermark_result.png')
            else:
                continue
        print('Hope to see you soon!')