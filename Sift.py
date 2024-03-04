import cv2
import numpy as np

# Load the images
image1 = cv2.imread('cam01.jpg')
image2 = cv2.imread('cam03.jpg')

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# Initialize and use FLANN based matcher
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# Apply Lowe's ratio test to filter matches
good_matches = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good_matches.append(m)

# Draw matches
result_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None)

# Display the result
cv2.imshow('Feature Matching', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
