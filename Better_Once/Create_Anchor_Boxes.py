import os
import numpy as np
from sklearn.cluster import KMeans


def load_bounding_box_dimensions(label_path):
    dimensions = []
    for label_file in os.listdir(label_path):
        full_path = os.path.join(label_path, label_file)
        with open(full_path, 'r') as f:
            for line in f.readlines():
                _, x_center, y_center, width, height = map(float, line.split())
                dimensions.append((width, height))
    return dimensions


def estimate_anchor_boxes(dimensions, num_anchors=9):
    kmeans = KMeans(n_clusters=num_anchors, random_state=0)
    kmeans.fit(dimensions)
    return kmeans.cluster_centers_


def main():
    dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov4_Structure\V2'  # Update this to your dataset root folder
    label_path = os.path.join(dataset_root, 'labels/train')  # Assuming we're using training labels to estimate

    # Load bounding box dimensions from label files
    dimensions = load_bounding_box_dimensions(label_path)
    # Estimate anchor boxes based on these dimensions
    anchor_boxes = estimate_anchor_boxes(dimensions)

    # Compute and sort the anchor boxes by area in descending order
    area = np.prod(anchor_boxes, axis=1)
    sorted_idxs = np.argsort(-area)  # Negative for descending sort
    sorted_anchor_boxes = anchor_boxes[sorted_idxs]

    # Split the sorted anchor boxes into three sets for YOLOv4's detection heads
    anchor_boxes_sets = np.array_split(sorted_anchor_boxes, 3)

    # Print the sorted and grouped anchor boxes
    print("Anchor boxes sorted and grouped for YOLOv4's detection heads:")
    for i, anchors in enumerate(anchor_boxes_sets, start=1):
        print(f"Detection Head {i}: {anchors}")


if __name__ == "__main__":
    main()
