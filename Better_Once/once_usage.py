from once import ONCE
import cv2
import os

# Initialize the ONCE dataset class with the root path of your dataset.
dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
output_directory = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Better_Once\Images'  # Replace with the directory where you want to save the images.
dataset = ONCE(dataset_root)

# Ensure the output directory exists.
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

seq_id = "000112"
frame_id = "1616534767199"

# Load point cloud and camera image.
points = dataset.load_point_cloud(seq_id, frame_id)

# Project LiDAR points onto camera images.
points_img_dict = dataset.project_lidar_to_image(seq_id, frame_id)

# Project 3D bounding boxes onto camera images.
boxes_img_dict = dataset.project_boxes_to_image(seq_id, frame_id)

# Loop through each camera and save images.
for cam_name in dataset.camera_names:
    # Save image with projected LiDAR points.
    if cam_name in points_img_dict:
        points_img_path = os.path.join(output_directory, f'lidar_projected_{cam_name}_{frame_id}.jpg')
        cv2.imwrite(points_img_path, cv2.cvtColor(points_img_dict[cam_name], cv2.COLOR_RGB2BGR))

    # Save image with projected bounding boxes.
    if cam_name in boxes_img_dict:
        boxes_img_path = os.path.join(output_directory, f'bounding_boxes_{cam_name}_{frame_id}.jpg')
        cv2.imwrite(boxes_img_path, cv2.cvtColor(boxes_img_dict[cam_name], cv2.COLOR_RGB2BGR))
