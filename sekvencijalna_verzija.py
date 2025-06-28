from PIL import Image
import math
import time 

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


def horizontal_blur(img, kernel):
    width, height = img.size
    pixels = img.load()
    radius = len(kernel) // 2
    new_img = Image.new("RGB", (width, height))
    new_pixels = new_img.load()

    for y in range(height):
        for x in range(width):
            r = g = b = 0.0
            for k in range(-radius, radius + 1): 
                px = x + k
                if px < 0:
                    px = 0
                elif px >= width:
                    px = width - 1
                pr, pg, pb = pixels[px, y] 
                weight = kernel[k + radius] 
                r += pr * weight
                g += pg * weight
                b += pb * weight
            new_pixels[x, y] = (int(r), int(g), int(b))
    return new_img

def vertical_blur(img, kernel):
    width, height = img.size
    pixels = img.load()
    radius = len(kernel) // 2
    new_img = Image.new("RGB", (width, height))
    new_pixels = new_img.load()

    for x in range(width):
        for y in range(height):
            r = g = b = 0.0
            for k in range(-radius, radius + 1):
                py = y + k
                if py < 0:
                    py = 0
                elif py >= height:
                    py = height - 1
                pr, pg, pb = pixels[x, py]
                weight = kernel[k + radius]
                r += pr * weight
                g += pg * weight
                b += pb * weight
            new_pixels[x, y] = (int(r), int(g), int(b))
    return new_img

def apply_gaussian_blur(image, radius):
    kernel = create_gaussian_kernel(radius)
    horizontal = horizontal_blur(image, kernel)
    vertical = vertical_blur(horizontal, kernel)
    return vertical


