# annotation_converter.py

import numpy as np
from config import BEV_WIDTH, BEV_HEIGHT, X_RANGE, Y_RANGE

def convert_3d_box_to_bev(box_3d, bev_dims, x_range, y_range):
    """
    Converts 3D bounding box annotations to BEV space.
    """
    # Extract 3D box parameters
    cx, cy, cz, l, w, h, rot = box_3d

    # Compute corners of 3D box
    corners = np.array([
        [cx - l / 2, cy - w / 2],
        [cx + l / 2, cy - w / 2],
        [cx + l / 2, cy + w / 2],
        [cx - l / 2, cy + w / 2]
    ])

    # Rotate corners around the Z-axis
    rot_matrix = np.array([
        [np.cos(rot), -np.sin(rot)],
        [np.sin(rot), np.cos(rot)]
    ])
    corners = np.dot(corners, rot_matrix)

    # Normalize the footprint coordinates to the BEV image dimensions
    x_norm = (corners[:, 0] - x_range[0]) / (x_range[1] - x_range[0])
    y_norm = (corners[:, 1] - y_range[0]) / (y_range[1] - y_range[0])

    # Convert normalized coordinates to pixels
    x_pixel = x_norm * bev_dims[0]
    y_pixel = y_norm * bev_dims[1]

    # Find min and max points to get bounding box in pixel coordinates
    x_min, x_max = min(x_pixel), max(x_pixel)
    y_min, y_max = min(y_pixel), max(y_pixel)

    # Calculate YOLO format: x_center, y_center, width, height (normalized)
    x_center = ((x_min + x_max) / 2) / bev_dims[0]
    y_center = ((y_min + y_max) / 2) / bev_dims[1]
    width = (x_max - x_min) / bev_dims[0]
    height = (y_max - y_min) / bev_dims[1]

    return [x_center, y_center, width, height]

def annotations_to_yolo(annotations, bev_dims, x_range, y_range):
    """
    Converts a list of 3D bounding box annotations to the YOLO format.
    """
    yolo_annotations = []
    for box_3d in annotations:
        yolo_box = convert_3d_box_to_bev(box_3d, bev_dims, x_range, y_range)
        yolo_annotations.append(yolo_box)
    return yolo_annotations
