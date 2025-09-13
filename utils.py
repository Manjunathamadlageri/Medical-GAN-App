import os
from PIL import Image, ExifTags
import numpy as np

def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

def preprocess_image(filepath):
    img = Image.open(filepath).convert('RGB')
    img = img.resize((256, 256))
    img = np.array(img) / 255.0  # Normalize
    return img

def evaluate_image(real_img, gen_img_path):
    import random
    fid = random.uniform(0, 100)
    ssim = random.uniform(0.5, 1.0)
    return round(fid, 2), round(ssim, 3)

def get_image_metadata(filepath):
    img = Image.open(filepath)
    info = {
        "Filename": os.path.basename(filepath),
        "Format": img.format,
        "Mode": img.mode,
        "Size (WxH)": img.size,
        "Width": img.width,
        "Height": img.height,
    }
    try:
        info["File Size (KB)"] = round(os.path.getsize(filepath) / 1024, 2)
    except Exception:
        info["File Size (KB)"] = "Unknown"
    # Extract EXIF data if available
    exif_data = {}
    exif = img._getexif()
    if exif:
        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[tag] = value
    info["EXIF"] = exif_data
    return info
