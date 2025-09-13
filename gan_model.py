import os
import numpy as np
from PIL import Image

def generate_synthetic_image(preprocessed_img, disease, output_folder):
    # Dummy GAN: just creates a random image
    fake_img = np.uint8(np.random.rand(256, 256, 3) * 255)
    img = Image.fromarray(fake_img)
    filename = f'synthetic_{disease}.png'
    img_path = os.path.join(output_folder, filename)
    img.save(img_path)
    return img_path
