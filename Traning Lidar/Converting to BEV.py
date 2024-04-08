from once import ONCE
import numpy as np
import cv2
import os
from glob import glob


def point_cloud_to_bev(points, x_range, y_range, z_range, bev_width, bev_height):
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


x_range = (-25, 25)  # meters
y_range = (-25, 25)  # meters
z_range = (-2, 1.5)  # meters relative to the LiDAR sensor position
bev_width = 608  # pixels
bev_height = 608  # pixels


def generate_bev_images(dataset, output_dir):
    # Assuming seq_id is provided. For example, '000076'
    seq_id = '000076'  # Replace with actual seq_id as needed

    # Construct the path to the lidar_roof directory
    lidar_path = os.path.join(dataset.data_root, seq_id, 'lidar_roof')

    print(lidar_path)

    # List all .bin files in the lidar_roof directory
    frame_files = glob(os.path.join(lidar_path, '*.bin'))

    print(frame_files)

    # Iterate over each frame file
    for frame_file in frame_files:
        # Extract frame_id from the file name
        frame_id = os.path.basename(frame_file).replace('.bin', '')

        # Load and preprocess point cloud to BEV
        points = dataset.load_point_cloud(seq_id, frame_id)
        bev_image = point_cloud_to_bev(points, x_range, y_range, z_range, bev_width, bev_height)

        # Save BEV image
        img_path = os.path.join(output_dir, f"{seq_id}_{frame_id}.png")
        cv2.imwrite(img_path, bev_image)


# Example usage
dataset = ONCE(dataset_root=r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet')
generate_bev_images(dataset, output_dir=r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Traning Lidar\Bev_Images')
