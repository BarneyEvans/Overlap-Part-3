import os
# config.py

# Paths to dataset and output directories
DATASET_ROOT = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\data'
OUTPUT_ROOT = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov4_Structure\V1'
STAGING_AREA = os.path.join(OUTPUT_ROOT, 'staging_area')

# BEV image dimensions
BEV_WIDTH = 608
BEV_HEIGHT = 608

# LiDAR range in meters
X_RANGE = (-25, 25)  # X-axis range
Y_RANGE = (-25, 25)  # Y-axis range
Z_RANGE = (-2, 1.5)  # Z-axis range relative to LiDAR sensor

# Training configuration
TRAIN_SIZE = 0.6
VAL_SIZE = 0.1
# Test size will be the remaining (1 - TRAIN_SIZE - VAL_SIZE)

# Path structure for the processed datasets
TRAIN_IMAGE_DIR = os.path.join(OUTPUT_ROOT, 'images', 'train')
VAL_IMAGE_DIR = os.path.join(OUTPUT_ROOT, 'images', 'val')
TEST_IMAGE_DIR = os.path.join(OUTPUT_ROOT, 'images', 'test')
TRAIN_LABEL_DIR = os.path.join(OUTPUT_ROOT, 'labels', 'train')
VAL_LABEL_DIR = os.path.join(OUTPUT_ROOT, 'labels', 'val')
TEST_LABEL_DIR = os.path.join(OUTPUT_ROOT, 'labels', 'test')
