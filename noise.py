import cv2
import rawpy
import matplotlib.pyplot as plt
import numpy as np


def hetero_gaussian_noise(img, alpha, delta):
    gaussian_noise = np.random.normal(0, alpha**2 * img + delta **2, img.shape)
    noisy_img = np.clip(img + gaussian_noise, 0, 255).astype(int)
    return noisy_img


if __name__ == '__main__':
    raw = rawpy.imread('data/imgs/noisy.CR2')
    rgb = raw.postprocess()

    plt.imshow(rgb)

    plt.show()
