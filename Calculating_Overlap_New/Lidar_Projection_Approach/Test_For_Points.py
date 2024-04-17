# test_frustums.py
from Main import frustum_1, frustum_2
from once import ONCE
import numpy as np
import cv2
import matplotlib.pyplot as plt

def create_simulated_point_cloud(frustum):
    points = np.hstack((frustum.frustum_corners, np.ones((frustum.frustum_corners.shape[0], 1))))  # Adding a dummy reflectance value
    return points

def save_point_cloud_as_bin(points, filename):
    points.astype(np.float32).tofile(filename)


def display_image(image, title="Camera Image"):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)  # Create a named window that can be resized
    cv2.imshow(title, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Show the image

    cv2.waitKey(0)  # Wait for a key press to close
    cv2.destroyWindow(title)  # Destroy the window after the key press


def main():
    # Path to your dataset root
    dataset_root = r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet"
    seq_id = "000076"
    frame_id = "1616343528200"

    # Initialize ONCE instance
    once_instance = ONCE(dataset_root)

    # Create point clouds for frustum corners and save as .bin files
    frustum_points_1 = create_simulated_point_cloud(frustum_1)
    frustum_points_2 = create_simulated_point_cloud(frustum_2)

    save_point_cloud_as_bin(frustum_points_1, 'frustum_1_points.bin')
    save_point_cloud_as_bin(frustum_points_2, 'frustum_2_points.bin')

    # Project these points using ONCE's functionality
    img_dict_1 = once_instance.project_lidar_to_image(seq_id, frame_id, 'frustum_1_points.bin')
    img_dict_2 = once_instance.project_lidar_to_image(seq_id, frame_id, 'frustum_2_points.bin')

    # Display results
    for cam_name, img in img_dict_1.items():
        display_image(img, title=f"Frustum 1 on {cam_name}")

    for cam_name, img in img_dict_2.items():
        display_image(img, title=f"Frustum 2 on {cam_name}")


if __name__ == '__main__':
    main()
