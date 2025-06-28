from PIL import Image
import math
import time
from multiprocessing import Pool

def create_gaussian_kernel(radius):
    sigma = radius / 3.0 if radius > 0 else 1.0
    size = 2 * radius + 1
    kernel = []
    sum_val = 0
    for i in range(-radius, radius + 1):
        val = (1 / (math.sqrt(2 * math.pi) * sigma)) * math.exp(-(i * i) / (2 * sigma * sigma))
        kernel.append(val)
        sum_val += val
    kernel = [x / sum_val for x in kernel]  
    return kernel

def blur_row_horizontal(args):
    y, row, kernel, radius = args
    length = len(row)
    result_row = [] 
    for x in range(length):
        r = g = b = 0.0
        for k in range(-radius, radius + 1):
            px = x + k
            if px < 0:
                px = 0
            elif px >= length:
                px = length - 1
            weight = kernel[k + radius]
            pr, pg, pb = row[px] 
            r += pr * weight
            g += pg * weight
            b += pb * weight
        result_row.append((int(r), int(g), int(b)))
    return y, result_row


def blur_column_vertical(args):
    x, col, kernel, radius = args
    length = len(col)
    result_col = []
    for y in range(length):
        r = g = b = 0.0
        for k in range(-radius, radius + 1):
            py = y + k
            if py < 0:
                py = 0
            elif py >= length:
                py = length - 1
            weight = kernel[k + radius]
            pr, pg, pb = col[py]
            r += pr * weight
            g += pg * weight
            b += pb * weight
        result_col.append((int(r), int(g), int(b)))
    return x, result_col

def horizontal_blur_parallel(img, kernel, radius):
    width, height = img.size
    pixels = img.load()

    
    args = [(y, [pixels[x, y] for x in range(width)], kernel, radius) for y in range(height)]

    with Pool() as pool:
        results = pool.map(blur_row_horizontal, args)

    results.sort(key=lambda x: x[0])

    new_img = Image.new("RGB", (width, height))
    new_pixels = new_img.load()

    for y, row in results:
        for x, pixel in enumerate(row):
            new_pixels[x, y] = pixel

    return new_img


def vertical_blur_parallel(img, kernel, radius):
    width, height = img.size
    pixels = img.load()

    args = [(x, [pixels[x, y] for y in range(height)], kernel, radius) for x in range(width)]

    with Pool() as pool:
        results = pool.map(blur_column_vertical, args)

    results.sort(key=lambda x: x[0])

    new_img = Image.new("RGB", (width, height))
    new_pixels = new_img.load()

    for x, col in results:
        for y, pixel in enumerate(col):
            new_pixels[x, y] = pixel

    return new_img


def apply_gaussian_blur_parallel(image, radius):
    kernel = create_gaussian_kernel(radius)
    horizontal = horizontal_blur_parallel(image, kernel, radius)
    vertical = vertical_blur_parallel(horizontal, kernel, radius)
    return vertical

