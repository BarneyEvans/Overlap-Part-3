import numpy as np
import cv2 as cv
import glob
from Cameras import Camera, camera5, camera6, camera7, camera8
import os
from matplotlib import pyplot as plt
from PIL import Image

image_paths = glob.glob('cam0[5-8].jpg')

print(image_paths)
images = {}

for path in image_paths:
    img = cv.imread(path)
    if img is not None:
        images[path] = img
    else:
        print(f'Warning: Could not read image at {path}')


def correct_distortion(image, camera):
    # Automatically undistorts image based on the intrinsic and etrinsic matrices
    undistorted_img = cv.undistort(image, camera.intrinsic_matrix, camera.distortion, None, camera.intrinsic_matrix)
    return undistorted_img


def stereo_vision(image1, image2, camera1, camera2):
    stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(image1, image2)
    plt.imshow(disparity,'gray')
    plt.show()




def feature_finder_sift(image1, image2):
    # Creates Sift detector
    sift = cv.SIFT_create()

    # Detect keypoints and compute descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    # Initialize and use FLANN based matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Apply Lowe's ratio test to filter matches7 and 8
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Draw matches
    result_image = cv.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None)
    cv.imwrite(os.path.join(r"C:\Users\be1g21\PycharmProjects\pythonProject\Overlap-Part-3" , 'Sift_Example.jpg'), result_image)
    # Display the result
    cv.imshow('Feature Matching', result_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


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

feature_finder_sift(camera7_distortion_corrected, camera8_distortion_corrected)
stereo_vision(images['cam07.jpg'], images['cam08.jpg'], camera7, camera8)


side_by_side = np.concatenate((camera7_distortion_corrected, camera8_distortion_corrected), axis=1)
cv.imshow('Undistorted Image', side_by_side)
# cv.imshow('Undistorted Image', camera8_distortion_corrected)
cv.waitKey(0)  # Wait indefinitely until a key is pressed
cv.destroyAllWindows()
