from PIL import Image, ImageDraw
import os
import cv2 as cv
from Cameras import camera5, camera6, camera7, camera8

def correct_distortion(image, camera):
    # Automatically undistorts image based on the intrinsic and etrinsic matrices
    undistorted_img = cv.undistort(image, camera.intrinsic_matrix, camera.distortion, None, camera.intrinsic_matrix)
    return undistorted_img

output_dir = "../Images/Undistorted_Images"

# Paths relative to the script location
first_image_path = "../Images/cam07.jpg"
second_image_path = "../Images/cam08.jpg"

image1 = cv.imread(first_image_path)
image2 = cv.imread(second_image_path)

correct1 = correct_distortion(image1, camera7)
correct2 = correct_distortion(image2, camera8)

correct_path1 = os.path.join(output_dir, 'cam07.jpg')
correct_path2 = os.path.join(output_dir, 'cam08.jpg')

cv.imwrite(correct_path1, correct1)
cv.imwrite(correct_path2, correct2)