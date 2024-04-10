import os
import exifread
import shutil
import random
import concurrent.futures
from PIL import Image
import rawpy
import imageio

source_folder = 'I:/IMGs_ALL/照片/7D'
destination_folder = './data/training'
raw_folder = './data/training/raw'
png_folder = './data/training/png'
iso_limit = 800


def check_iso(filepath):
    """
    :param filepath: path of the file to check
    :return:
    """
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        iso = tags.get('EXIF ISOSpeedRatings')
        if iso and int(iso.values[0]) < iso_limit:
            return filepath
        else:
            return None


def random_copy_imgs(src, dest, n):
    """
    :param src: Source folder where all images are loacted
    :param dest: Destination folder to copy images to
    :param n: number of images to copy
    :return:
    """
    eligible_files = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for dir_path, dir_names, filenames in os.walk(src):
            cr2_files = [os.path.join(dir_path, f) for f in filenames if f.endswith('.CR2')]
            eligible_files.extend(list(filter(None, executor.map(check_iso, cr2_files))))

    files_to_copy = random.sample(eligible_files, n)
    for file in files_to_copy:
        shutil.copy(file, dest)


def split_img(img, patch_size, idx):
    width, height = img.size
    for i in range(0, width, patch_size):
        for j in range(0, height, patch_size):
            if i + patch_size <= width and j + patch_size <= height:
                box = (i, j, i+patch_size, j+patch_size)
                yield img.crop(box), f"{img_idx}-{i//patch_size}-{j//patch_size}"


if __name__ == '__main__':
    # Randomly Select 100 Imgs from my folder
    # random_copy_imgs(source_folder, raw_folder, 100)

    img_idx = 0
    for filename in os.listdir(raw_folder):
        if filename.endswith('.CR2'):
            src_path = os.path.join(raw_folder, filename)
            with rawpy.imread(src_path) as raw:
                rgb = raw.postprocess()
            imageio.imsave(os.path.join(png_folder, filename.replace("CR2", "png")), rgb)
        # if filename.endswith('.CR2'):
        #     path = os.path.join(destination_folder+"/raw", filename)
        #     with Image.open(path) as img:
        #         for patch, patch_name in split_img(img, 512, img_idx):
        #             patch.save(os.path.join(destination_folder+"/clean", f"{patch_name}.png"))
        #     img_idx += 1

