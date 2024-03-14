import json
import os
# Load the JSON file into a Python dictionary
json_file_path = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\000076.json'
with open(json_file_path, 'r') as file:
    data_dict = json.load(file)

frames = data_dict["frames"]  # Assuming this is the correct path within your loaded JSON structure

def save_annotations_for_cam(frames, output_dir, camera, class_mapping, image_dimensions):
    """
    Save annotations for a specific camera from frame data to .txt files,
    only for frames that contain annotation data.

    :param frames: List of frame data including frame_id, and annotations.
    :param output_dir: Directory where annotation .txt files will be saved.
    :param camera: Specific camera ID for which annotations are to be saved.
    :param class_mapping: Dictionary mapping class names to class IDs.
    :param image_dimensions: Tuple of (image_width, image_height) for normalization.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for frame in frames:
        frame_id = frame.get("frame_id")
        annotations = frame.get("annos", {})
        names = annotations.get("names", [])
        boxes_2d = annotations.get("boxes_2d", {}).get(camera, [])

        # Proceed only if there are bounding boxes for the specified camera
        if not boxes_2d or all(box[0] == -1.0 for box in boxes_2d):
            continue

        with open(os.path.join(output_dir, f"{frame_id}.txt"), 'w') as file:
            for name, box_2d in zip(names, boxes_2d):
                if box_2d[0] == -1.0:  # Skip invalid boxes
                    continue
                class_id = class_mapping.get(name)
                if class_id is not None and image_dimensions:
                    # Normalize coordinates
                    x_center = (box_2d[0] + box_2d[2]) / 2 / image_dimensions[0]
                    y_center = (box_2d[1] + box_2d[3]) / 2 / image_dimensions[1]
                    width = (box_2d[2] - box_2d[0]) / image_dimensions[0]
                    height = (box_2d[3] - box_2d[1]) / image_dimensions[1]

                    file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

# Load your JSON file
json_file_path = 'C:/Users/be1g21/OneDrive - University of Southampton/Desktop/Year 3/Year 3 Project/Dataset/data_root/data.json'
# Example usage parameters
output_dir = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam08\Yolo_Info'  # Specify your output directory
camera = "cam08"  # This should match the camera you want to process in the frames
class_mapping = {"Car": 0, "Truck": 1, "Cyclist": 2, "Pedestrian": 3, "Bus": 4}  # Your specific class mapping
image_dimensions = (1920, 1020)  # Actual dimensions for images from "cam01"

# Call the function with loaded frames data
save_annotations_for_cam(frames, output_dir, camera, class_mapping, image_dimensions)
