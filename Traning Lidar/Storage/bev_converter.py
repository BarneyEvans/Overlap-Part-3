# bev_converter.py

import numpy as np
import cv2
from config import X_RANGE, Y_RANGE, Z_RANGE, BEV_WIDTH, BEV_HEIGHT

def filter_points(points, x_range, y_range, z_range):
    """
    Filter point cloud points based on the specified ranges.
    """
    x_filter = (points[:, 0] >= x_range[0]) & (points[:, 0] <= x_range[1])
    y_filter = (points[:, 1] >= y_range[0]) & (points[:, 1] <= y_range[1])
    z_filter = (points[:, 2] >= z_range[0]) & (points[:, 2] <= z_range[1])
    filter = x_filter & y_filter & z_filter
    return points[filter]

def scale_to_image(points, x_range, y_range, width, height):
    """
    Scale the filtered point cloud points to the image plane.
    """
    x_img = ((points[:, 0] - x_range[0]) / (x_range[1] - x_range[0])) * width
    y_img = ((points[:, 1] - y_range[0]) / (y_range[1] - y_range[0])) * height
    return np.stack((x_img, y_img), axis=1)

def point_cloud_to_bevvy(points, x_range, y_range, z_range, bev_width, bev_height):
    # Filter points within the specified ranges
    mask = np.all((points[:, 0] >= x_range[0], points[:, 0] <= x_range[1],
                   points[:, 1] >= y_range[0], points[:, 1] <= y_range[1],
                   points[:, 2] >= z_range[0], points[:, 2] <= z_range[1]), axis=0)
    points = points[mask]

    # Convert to BEV space
    x_img = ((points[:, 0] - x_range[0]) / (x_range[1] - x_range[0]) * bev_width).astype(np.int32)
    y_img = ((points[:, 1] - y_range[0]) / (y_range[1] - y_range[0]) * bev_height).astype(np.int32)

    # Initialize BEV image
    bev_image = np.zeros((bev_height, bev_width), dtype=np.uint8)

    # Populate BEV image
    bev_image[y_img, x_img] = 255  # Example: set occupied cells to 255 (white)

    return bev_image

def point_cloud_to_bev(points):
    """
    Wrapper function to create a BEV image from raw point cloud data.
    """
    return point_cloud_to_bevvy(points, X_RANGE, Y_RANGE, Z_RANGE, BEV_WIDTH, BEV_HEIGHT)
