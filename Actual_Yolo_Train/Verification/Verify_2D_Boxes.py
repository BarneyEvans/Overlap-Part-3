import cv2
import matplotlib.pyplot as plt
from once import ONCE


def read_label_file(label_file_path):
    """
    Reads a label file and returns a list of bounding boxes and class IDs.

    Args:
    - label_file_path: Path to the label file.

    Returns:
    - A list of tuples, each representing a bounding box and class ID: (class_id, x_center, y_center, width, height)
    """
    with open(label_file_path, 'r') as file:
        lines = file.readlines()
    boxes = [tuple(map(float, line.split())) for line in lines]
    return boxes


def plot_bounding_box(seq_id, frame_id, cam_name, dataset, label_file_path, image_dimensions):
    """
    Plots bounding boxes and class IDs on the undistorted image.

    Args:
    - seq_id: Sequence ID of the image.
    - frame_id: Frame ID of the image.
    - cam_name: Camera name as per dataset.
    - dataset: ONCE object with loaded dataset.
    - label_file_path: Path to the label file containing bounding boxes and class IDs.
    - image_dimensions: The dimensions of the image as a tuple (width, height).
    """
    # Undistort the image
    img_list, new_cam_intrinsic_dict = dataset.undistort_image_v2(seq_id, frame_id)
    camera_index = ONCE.camera_names.index(cam_name)
    undistorted_image = img_list[camera_index]

    # Read bounding boxes from the label file
    boxes = read_label_file(label_file_path)

    for box in boxes:
        class_id, x_center, y_center, width, height = box
        # Convert from normalized to pixel values using the new camera matrix
        new_cam_intrinsic = new_cam_intrinsic_dict[cam_name]
        x_center, y_center, width, height = (
            x_center * image_dimensions[0],
            y_center * image_dimensions[1],
            width * image_dimensions[0],
            height * image_dimensions[1]
        )
        # Calculate the top-left corner
        top_left = (int(x_center - width / 2), int(y_center - height / 2))
        bottom_right = (int(x_center + width / 2), int(y_center + height / 2))

        # Draw rectangle and class ID on the undistorted image
        cv2.rectangle(undistorted_image, top_left, bottom_right, (255, 0, 0), 2)
        cv2.putText(undistorted_image, str(class_id), top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the image
    plt.imshow(cv2.cvtColor(undistorted_image, cv2.COLOR_BGR2RGB))
    plt.show()


# Example usage
# Example usage
data = ONCE(dataset_root=r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet')
seq_id = "000112"  # Replace with your actual seq_id
frame_id = "1616535305201"  # Replace with your actual frame_id
cam_name = "cam03"  # Replace with the camera name you want to use
label_file_path = r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\temp\cam03_1616535305201.txt"
image_dimensions = (1920, 1080)  # Replace with your actual image dimensions

plot_bounding_box(seq_id, frame_id, cam_name, data, label_file_path, image_dimensions)

