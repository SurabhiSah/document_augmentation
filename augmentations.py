import cv2
import numpy as np

def flip_image(image):
    return cv2.flip(image, 1)

def rotate_image(image, angle=15):
    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def scale_image(image, fx=1.2, fy=1.2):
    return cv2.resize(image, None, fx=fx, fy=fy)

def translate_image(image, tx=25, ty=25):
    M = np.array([[1, 0, tx], [0, 1, ty]], dtype=np.float32)
    return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

def add_noise(image):
    row, col, ch = image.shape
    mean = 0
    stddev = 25
    noise = np.random.normal(mean, stddev, (row, col, ch)).astype('uint8')
    noisy_image = cv2.add(image, noise)
    return noisy_image

def shear_image(image):
    rows, cols = image.shape[:2]
    M = np.array([[1, 0.2, 0], [0.2, 1, 0]], dtype=np.float32)
    return cv2.warpAffine(image, M, (cols, rows))
