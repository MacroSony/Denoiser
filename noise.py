import cv2
import rawpy
import matplotlib.pyplot as plt
import numpy as np


def hetero_gaussian_noise(img, alpha, delta):
    gaussian_noise = np.random.normal(0, alpha**2 * img + delta **2, img.shape)
    noisy_img = np.clip(img + gaussian_noise, 0, 255).astype(int)
    # print(noisy_img)
    return noisy_img


# raw = rawpy.imread('data/imgs/clean.CR2')
raw = rawpy.imread('data/imgs/noisy.CR2')
rgb = raw.postprocess()

# noisy = hetero_gaussian_noise(rgb, 0.5, 5)

# print(type(noisy), noisy.shape, noisy)

# half = cv2.resize(noisy, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)

plt.imshow(rgb)

plt.show()
