import json
import os
import numpy as np
from once import ONCE
import cv2
# Assuming once.py is in the same directory or the module is installed.

# Configuration
dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
output_dir = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Traning Lidar\Labelled_Bev_Images'
bev_image_dir = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Traning Lidar\Bev_Images'
bev_dims = (608, 608)  # BEV image dimensions
lidar_range = [(-25, 25), (-25, 25)]  # LiDAR x and y range in meters
x_range, y_range = lidar_range

# Mapping from class names in the ONCE dataset to class IDs for YOLO
class_name_to_id = {
    "Car": 0,
    "Truck": 1,
    "Bus": 2,
    "Cyclist": 3,
    "Pedestrian": 4,
    # ... add other classes as needed ...
}


# Function to convert 3D box annotations to BEV space and then normalize them for YOLO
def convert_3d_box_to_bev(box_3d, bev_dims, lidar_range):
    # Extract 3D box parameters
    cx, cy, cz, l, w, h, rot = box_3d
    # Compute the footprint of the 3D box on the BEV image
    bev_box = np.array([[cx - l / 2, cy - w / 2], [cx + l / 2, cy + w / 2]])

    # Normalize the footprint coordinates to the BEV image dimensions
    bev_box[:, 0] = (bev_box[:, 0] - lidar_range[0][0]) / (lidar_range[0][1] - lidar_range[0][0]) * bev_dims[0]
    bev_box[:, 1] = (bev_box[:, 1] - lidar_range[1][0]) / (lidar_range[1][1] - lidar_range[1][0]) * bev_dims[1]

    x_min, x_max, y_min, y_max = bev_box[:, 0].min(), bev_box[:, 0].max(), bev_box[:, 1].min(), bev_box[:, 1].max()

    # Calculate YOLO format: x_center, y_center, width, height (normalized)
    x_center = ((x_min + x_max) / 2) / bev_dims[0]
    y_center = ((y_min + y_max) / 2) / bev_dims[1]
    width = (x_max - x_min) / bev_dims[0]
    height = (y_max - y_min) / bev_dims[1]

    return [x_center, y_center, width, height]


def draw_bev_boxes(image_path, boxes, output_path):
    # Load the BEV image
    bev_image = cv2.imread(image_path)

    # Check if the image was successfully loaded
    if bev_image is None:
        print(f"Error: Image at {image_path} could not be loaded.")
        return

    # Draw each box on the BEV image
    for box in boxes:
        class_id, x_center, y_center, width, height = box
        # Convert normalized positions back to pixel positions
        x_center_pixel = int(x_center * bev_dims[0])
        y_center_pixel = int(y_center * bev_dims[1])
        width_pixel = int(width * bev_dims[0])
        height_pixel = int(height * bev_dims[1])

        # Calculate the top left corner of the rectangle
        top_left = (x_center_pixel - width_pixel // 2, y_center_pixel - height_pixel // 2)
        # Calculate the bottom right corner of the rectangle
        bottom_right = (x_center_pixel + width_pixel // 2, y_center_pixel + height_pixel // 2)

        # Draw the rectangle on the image
        color = (0, 255, 0) if class_id == 0 else (0, 0, 255)  # Example: Green for cars, Red otherwise
        cv2.rectangle(bev_image, top_left, bottom_right, color, 2)

    # Save or display the result
    cv2.imwrite(output_path, bev_image)
    # cv2.imshow("BEV with Boxes", bev_image)  # Uncomment this to display the image
    # cv2.waitKey(0)  # Uncomment this to wait until a key is pressed before continuing


# Function to save annotations in YOLO format
def save_annotations(annotations, output_path):
    with open(output_path, 'w') as file:
        for annotation in annotations:
            file.write(" ".join(map(str, annotation)) + "\n")

dataset = ONCE(dataset_root=dataset_root)
# Iterate over the sequence IDs from the train split list
for seq_id in dataset.train_split_list:
    json_path = os.path.join(dataset.data_root, seq_id, f"{seq_id}.json")

    # Check if the annotation JSON file exists
    if not os.path.isfile(json_path):
        continue

    with open(json_path, 'r') as file:
        data = json.load(file)

    for frame in data['frames']:
        # Skip frames without annotations
        if 'annos' not in frame:
            continue

        frame_id = frame['frame_id']
        annotations = []

        for name, box_3d in zip(frame['annos']['names'], frame['annos']['boxes_3d']):
            if name not in class_name_to_id:
                continue

            class_id = class_name_to_id[name]
            normalized_bev_box = convert_3d_box_to_bev(box_3d, bev_dims, lidar_range)
            annotations.append([class_id] + normalized_bev_box)

        if annotations:
            # Assume your BEV images are named in the format "{seq_id}_{frame_id}.png"
            bev_image_path = os.path.join(bev_image_dir, f"{seq_id}_{frame_id}.png")
            label_output_path = os.path.join(output_dir, f"{seq_id}_{frame_id}_labeled.png")
            draw_bev_boxes(bev_image_path, annotations, label_output_path)