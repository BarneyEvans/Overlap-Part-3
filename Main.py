import numpy as np
import cv2 as cv
import glob
from Cameras import Camera, camera5, camera6, camera7, camera8
from PIL import Image

image_paths = glob.glob('cam0[5-8].jpg')

print(image_paths)
images = {}

# Loop through each path, read the image, and add it to the list
for path in image_paths:
    img = cv.imread(path)  # Read the image
    if img is not None:
        images[path] = img  # Add the image to the list
    else:
        print(f'Warning: Could not read image at {path}')


def correct_distortion(image, camera):
    undistorted_img = cv.undistort(image, camera.intrinsic_matrix, camera.distortion, None, camera.intrinsic_matrix)
    return undistorted_img


def transform_points(points, transformation_matrix):
    pass


def project_points_to_image(points, camera_intrinsics):
    pass


def calculate_overlap(camera1_data, camera2_data):
    pass


def display_overlap(image, overlap_area):
    pass


camera5_distortion_corrected = correct_distortion(images['cam05.jpg'], camera5)
camera6_distortion_corrected = correct_distortion(images['cam06.jpg'], camera6)
camera7_distortion_corrected = correct_distortion(images['cam07.jpg'], camera7)
camera8_distortion_corrected = correct_distortion(images['cam08.jpg'], camera8)

side_by_side = np.concatenate((camera7_distortion_corrected, camera8_distortion_corrected), axis=1)
cv.imshow('Undistorted Image', side_by_side)
#cv.imshow('Undistorted Image', camera8_distortion_corrected)
cv.waitKey(0)  # Wait indefinitely until a key is pressed
cv.destroyAllWindows()
