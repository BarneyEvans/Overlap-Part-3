import cv2
import os

def convert_yolo_to_pixel(box, image_shape):
    """
    Convert YOLO format bounding box (normalized) to pixel format.
    """
    img_height, img_width = image_shape[:2]
    x_center, y_center, width, height = box
    x_center, y_center, width, height = float(x_center), float(y_center), float(width), float(height)

    x1 = int((x_center - width / 2) * img_width)
    y1 = int((y_center - height / 2) * img_height)
    x2 = int((x_center + width / 2) * img_width)
    y2 = int((y_center + height / 2) * img_height)

    return x1, y1, x2, y2

def draw_bounding_boxes(image_path, label_path):
    """
    Draw bounding boxes from a label file onto the corresponding image.
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image '{image_path}'")
        return

    # Read label file and draw each bounding box
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id, x_center, y_center, width, height = parts[0], parts[1], parts[2], parts[3], parts[4]
            box = convert_yolo_to_pixel([x_center, y_center, width, height], image.shape)
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(image, class_id, (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Save or display the image
    output_path = 'output_image.jpg'  # Specify the output path
    cv2.imwrite(output_path, image)
    # Optionally, display the image
    # cv2.imshow('Image with Bounding Boxes', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print(f"Output saved to '{output_path}'")

# Example usage
image_path = r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\images\val\000112_cam07_1616534767199.jpg"  # Update this path
label_path = r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\labels\val\000112_cam07_1616534767199.txt"  # Update this path
draw_bounding_boxes(image_path, label_path)
