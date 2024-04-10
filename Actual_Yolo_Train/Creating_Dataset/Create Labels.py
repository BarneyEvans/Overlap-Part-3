import json
import os
import logging
import random
import shutil

def get_full_dataset_base_path():
    return r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'

def load_json_annotations(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

def convert_bbox_to_yolo(box, image_dimensions):
    x1, y1, x2, y2 = box
    width, height = image_dimensions
    dw = 1. / width
    dh = 1. / height
    x = (x1 + x2) / 2.0 - x1
    y = (y1 + y2) / 2.0 - y1
    w = x2 - x1
    h = y2 - y1
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def save_yolo_annotations(annotations, output_dir, class_mapping, image_dimensions, cameras):
    os.makedirs(output_dir, exist_ok=True)
    for frame in annotations.get("frames", []):
        frame_id = frame["frame_id"]
        for camera in cameras:
            if camera not in frame.get("annos", {}).get("boxes_2d", {}):
                continue
            boxes_2d = frame.get("annos", {}).get("boxes_2d", {}).get(camera, [])
            if not boxes_2d:
                continue
            output_file_path = os.path.join(output_dir, f"{camera}_{frame_id}.txt")
            with open(output_file_path, 'w') as file:
                for name, box in zip(frame.get("annos", {}).get("names", []), boxes_2d):
                    if name not in class_mapping or box[0] == -1.0:
                        continue  # Skip if class not recognized or invalid box
                    class_id = class_mapping[name]
                    x_center, y_center, width, height = convert_bbox_to_yolo(box, image_dimensions)
                    file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
                logging.info(f"Annotations saved to {output_file_path}")

def copy_images_to_split_dirs(sequence_id, cameras, source_dir, dest_dir_base, split):
    for camera in cameras:
        src_camera_dir = os.path.join(source_dir, sequence_id, camera)
        if not os.path.exists(src_camera_dir):
            continue
        dest_dir = os.path.join(dest_dir_base, split, camera)
        os.makedirs(dest_dir, exist_ok=True)
        for image_file in os.listdir(src_camera_dir):
            src_file_path = os.path.join(src_camera_dir, image_file)
            dest_file_path = os.path.join(dest_dir, image_file)
            if os.path.isfile(src_file_path):
                shutil.copy2(src_file_path, dest_file_path)
                logging.info(f"Copied {src_file_path} to {dest_file_path}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    full_dataset_base = get_full_dataset_base_path()
    data_dir = os.path.join(full_dataset_base, 'data')

    yolov8_images_base = os.path.join(full_dataset_base, "Yolov8 Structure", "V2", "dataset", "images")
    yolov8_labels_base = os.path.join(full_dataset_base, "Yolov8 Structure", "V2", "dataset", "labels")

    class_mapping = {"Car": 0, "Truck": 1, "Cyclist": 2, "Pedestrian": 3, "Bus": 4}
    image_dimensions = (1920, 1080)  # Assuming all images have the same dimensions
    cameras = ["cam01", "cam02", "cam03", "cam04"]  # List your cameras here

    all_sequence_ids = [seq_id for seq_id in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, seq_id))]
    random.shuffle(all_sequence_ids)

    num_sequences = len(all_sequence_ids)
    train_end = int(num_sequences * 0.8)
    val_end = train_end + int(num_sequences * 0.1)


    train_ids = all_sequence_ids[:train_end]
    val_ids = all_sequence_ids[train_end:val_end]
    test_ids = all_sequence_ids[val_end:]
    print(len(train_ids), len(val_ids), len(test_ids))
    return
    for split, sequence_ids in [("train", train_ids), ("val", val_ids), ("test", test_ids)]:
        for sequence_id in sequence_ids:
            json_path = os.path.join(data_dir, sequence_id, f"{sequence_id}.json")
            if not os.path.isfile(json_path):
                logging.warning(f"JSON file not found for sequence ID: {sequence_id}")
                continue
            annotations = load_json_annotations(json_path)
            output_label_dir = os.path.join(yolov8_labels_base, split)
            save_yolo_annotations(annotations, output_label_dir, class_mapping, image_dimensions, cameras)
            copy_images_to_split_dirs(sequence_id, cameras, data_dir, yolov8_images_base, split)

    logging.info("Processing complete.")

if __name__ == "__main__":
    main()
