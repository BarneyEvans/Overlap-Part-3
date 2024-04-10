from once import ONCE
import numpy as np
import cv2
import os
from glob import glob
import json

class_name_to_id = {
    "Car": 0,
    "Truck": 1,
    "Bus": 2,
    "Cyclist": 3,
    "Pedestrian": 4,
}

x_range = (-25, 25)  # meters
y_range = (-25, 25)  # meters
z_range = (-5, 5)  # meters relative to the LiDAR sensor position
bev_width, bev_height = 1024, 1024  # Example of increased resolution
bev_dims = (bev_width, bev_height)  # BEV image dimensions
lidar_range = [(-25, 25), (-25, 25)]  # LiDAR x and y range in meters


def generate_bev_images_and_labels(dataset, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sequences = ["000076"]
    selected_folder = 'test'  # Directly set to 'test'

    for seq_id in sequences:
        lidar_path = os.path.join(dataset.data_root, seq_id, 'lidar_roof')
        label_file_path = os.path.join(dataset.data_root, seq_id, f"{seq_id}.json")

        # Verify annotation file exists
        if not os.path.isfile(label_file_path):
            print(f"Annotation file {label_file_path} not found, skipping.")
            continue

        annotations_dict = handle_json(label_file_path)

        # Specifying a single frame
        frame_file = os.path.join(lidar_path, '1616343528200.bin')
        if not os.path.isfile(frame_file):
            print(f"Frame file {frame_file} not found, skipping.")
            continue

        frame_id = '1616343528200'  # Directly use the frame ID

        # Process the frame if annotations are present
        if frame_id in annotations_dict:
            points = dataset.load_point_cloud(seq_id, frame_id)
            bev_image = point_cloud_to_bev(points, x_range, y_range, z_range, bev_width, bev_height)

            # Preparing paths for saving images and labels
            image_folder_path = os.path.join(output_dir, 'images', selected_folder)
            label_folder_path = os.path.join(output_dir, 'labels', selected_folder)

            # Ensure subfolders exist
            for path in [image_folder_path, label_folder_path]:
                if not os.path.exists(path):
                    os.makedirs(path)

            # Saving BEV image
            img_path = os.path.join(image_folder_path, f"{seq_id}_{frame_id}.png")
            img_path = handle_filename_conflict(img_path)  # Handle filename conflict
            cv2.imwrite(img_path, bev_image)

            # Saving corresponding labels
            label_path = os.path.join(label_folder_path, f"{seq_id}_{frame_id}.txt")
            label_path = handle_filename_conflict(label_path)  # Handle filename conflict
            save_annotations(label_path, annotations_dict[frame_id])

def handle_filename_conflict(file_path):
    # If file already exists, append a letter before the extension until a unique filename is found
    base_path, extension = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base_path}_{chr(96 + counter)}{extension}"  # Appending a letter (a, b, c, ...) before the extension
        counter += 1
    return file_path

def save_annotations(label_file, annotations):
    with open(label_file, 'w') as f:
        for annotation in annotations:
            f.write(' '.join(map(str, annotation)) + '\n')


def handle_json(label_file):
    with open(label_file, 'r') as file:
        data = json.load(file)
    annotations_dict = {}
    for frame in data.get('frames', []):
        frame_id = frame.get('frame_id')
        if 'annos' in frame:
            annotations = []
            for name, box_3d in zip(frame['annos'].get('names', []), frame['annos'].get('boxes_3d', [])):
                if name in class_name_to_id:
                    class_id = class_name_to_id[name]
                    normalized_bev_box = convert_3d_box_to_bev(box_3d, bev_dims, lidar_range)
                    annotations.append([class_id] + normalized_bev_box)
            if annotations:
                annotations_dict[frame_id] = annotations
    return annotations_dict


def point_cloud_to_bev(points, x_range, y_range, z_range, bev_width, bev_height):
    # Filter points within the specified ranges
    mask = np.all((points[:, 0] >= x_range[0], points[:, 0] <= x_range[1],
                   points[:, 1] >= y_range[0], points[:, 1] <= y_range[1],
                   points[:, 2] >= z_range[0], points[:, 2] <= z_range[1]), axis=0)
    points = points[mask]

    # Convert to BEV space
    x_img = ((points[:, 0] - x_range[0]) / (x_range[1] - x_range[0]) * bev_width).astype(np.int32)
    y_img = ((points[:, 1] - y_range[0]) / (y_range[1] - y_range[0]) * bev_height).astype(np.int32)

    # Ensure indices are within bounds
    x_img = np.clip(x_img, 0, bev_width - 1)
    y_img = np.clip(y_img, 0, bev_height - 1)

    # Initialize BEV image
    bev_image = np.zeros((bev_height, bev_width), dtype=np.uint8)

    # Populate BEV image
    bev_image[y_img, x_img] = 255  # Set occupied cells to 255 (white)

    return bev_image



def convert_3d_box_to_bev(box_3d, bev_dims, lidar_range):
    # Extract 3D box parameters
    cx, cy, cz, l, w, h, rot = box_3d
    # cmCompute the footprint of the 3D box on the BEV image
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

# Example usage
dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
output_dir = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Better_Once\Bev_Test'
dataset = ONCE(dataset_root=dataset_root)
generate_bev_images_and_labels(dataset, output_dir)
