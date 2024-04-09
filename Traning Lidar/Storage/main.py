# main.py

from data_loader import load_annotations, load_point_cloud
from bev_converter import point_cloud_to_bev
from annotation_converter import annotations_to_yolo
from dataset_splitter import run_split
from config import DATASET_ROOT, OUTPUT_ROOT, X_RANGE, Y_RANGE, Z_RANGE, BEV_WIDTH, BEV_HEIGHT

import os
import json
import cv2


def process_sequence(sequence_id):
    """
    Process a single sequence of data.
    """
    # Load annotations for the sequence
    annotations = load_annotations(sequence_id)

    # Process each frame in the sequence
    for frame in annotations['frames']:
        frame_id = frame['frame_id']

        # Check if frame contains annotations (i.e., is not empty)
        if 'annos' not in frame:
            continue

        # Load and convert point cloud to BEV
        points = load_point_cloud(sequence_id, frame_id)
        bev_image = point_cloud_to_bev(points)

        # Convert annotations to YOLO format
        yolo_annos = annotations_to_yolo(frame['annos']['boxes_3d'], (BEV_WIDTH, BEV_HEIGHT), X_RANGE, Y_RANGE)

        # Save BEV image and annotations
        bev_image_path = os.path.join(OUTPUT_ROOT, 'bev_images', f"{sequence_id}_{frame_id}.png")
        label_path = os.path.join(OUTPUT_ROOT, 'labels', f"{sequence_id}_{frame_id}.txt")

        cv2.imwrite(bev_image_path, bev_image)
        with open(label_path, 'w') as label_file:
            for anno in yolo_annos:
                label_file.write(' '.join(map(str, anno)) + '\n')


def main():
    """
    Main function to process the dataset and prepare for training.
    """
    # Get list of sequence IDs from dataset
    sequence_ids = [name for name in os.listdir(DATASET_ROOT) if os.path.isdir(os.path.join(DATASET_ROOT, name))]

    # Process each sequence
    for sequence_id in sequence_ids:
        process_sequence(sequence_id)

    # After all sequences are processed, split the dataset
    run_split()


if __name__ == '__main__':
    main()
