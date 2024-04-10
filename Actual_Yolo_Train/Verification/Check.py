import os

def gather_files_by_split(base_path, splits):
    """Gathers files by split, removing file extensions for comparison."""
    files_by_split = {}
    for split in splits:
        dir_path = os.path.join(base_path, split)
        files = {os.path.splitext(f)[0] for f in os.listdir(dir_path)}
        files_by_split[split] = files
    return files_by_split

def analyze_distributions(images_base, labels_base):
    splits = ['train', 'val', 'test']
    images_by_split = gather_files_by_split(images_base, splits)
    labels_by_split = gather_files_by_split(labels_base, splits)

    summary = {
        split: {
            'images_without_annotations': [],
            'annotations_without_images': [],
            'misclassified_images': [],
            'misclassified_annotations': []
        } for split in splits
    }

    all_labels = set.union(*labels_by_split.values())
    all_images = set.union(*images_by_split.values())

    for split in splits:
        other_splits = splits[:]
        other_splits.remove(split)

        # Images without annotations in the same split
        summary[split]['images_without_annotations'] = list(images_by_split[split] - labels_by_split[split])

        # Annotations without images in the same split
        summary[split]['annotations_without_images'] = list(labels_by_split[split] - images_by_split[split])

        # Misclassified images: images in the current split but have annotations in a different split
        misclassified_images = set()
        for other in other_splits:
            misclassified_images |= (images_by_split[split] & labels_by_split[other])
        summary[split]['misclassified_images'] = list(misclassified_images)

        # Misclassified annotations: annotations in the current split but images in a different split
        misclassified_annotations = set()
        for other in other_splits:
            misclassified_annotations |= (labels_by_split[split] & images_by_split[other])
        summary[split]['misclassified_annotations'] = list(misclassified_annotations)

    # Images and annotations that do not belong in any split
    for split in splits:
        summary[split]['orphan_images'] = list(images_by_split[split] - all_labels)
        summary[split]['orphan_annotations'] = list(labels_by_split[split] - all_images)

    return summary

def main():
    images_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\images'
    labels_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\labels'

    summary = analyze_distributions(images_base, labels_base)

    for split, data in summary.items():
        print(f"--- {split.upper()} ---")
        print(f"Images without annotations: {len(data['images_without_annotations'])}")
        print(f"Annotations without images: {len(data['annotations_without_images'])}")
        print(f"Misclassified images: {len(data['misclassified_images'])}")
        print(f"Misclassified annotations: {len(data['misclassified_annotations'])}")
        print(f"Orphan images (no annotations in any split): {len(data['orphan_images'])}")
        print(f"Orphan annotations (no images in any split): {len(data['orphan_annotations'])}")
        print()

if __name__ == "__main__":
    main()
