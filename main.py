from PIL import Image
import time

from paralelna_verzija import apply_gaussian_blur_parallel
from sekvencijalna_verzija import apply_gaussian_blur

if __name__ == "__main__":
    path = "C:/Users/Lenovo/Desktop/converted-image.png"
    img = Image.open(path).convert("RGB")
    radius = 50

    # SEKVENCIJALNO
    start_seq = time.time()
    result_seq = apply_gaussian_blur(img, radius)
    end_seq = time.time()
    trajanje_seq = (end_seq - start_seq) * 1000
    result_seq.save("C:/Users/Lenovo/Desktop/rezultat_sekvencijalno.png")
    print(f"Sekvencijalna obrada: {trajanje_seq:.0f} ms")

    # PARALELNO
    img = Image.open(path).convert("RGB")  
    start_par = time.time()
    result_par = apply_gaussian_blur_parallel(img, radius)
    end_par = time.time()
    trajanje_par = (end_par - start_par) * 1000
    result_par.save("C:/Users/Lenovo/Desktop/rezultat_paralelno.png")
    print(f"Paralelna obrada: {trajanje_par:.0f} ms")
