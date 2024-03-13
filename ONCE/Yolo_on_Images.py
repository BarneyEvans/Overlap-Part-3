from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
import os

def detect_and_save(image_path, output_path, model):
    img = cv2.imread(image_path)
    results = model.predict(img)

    annotator = Annotator(img)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)])


    annotated_img = annotator.result()
    cv2.imwrite(output_path, annotated_img)
    print(f"Detection result saved to {output_path}")


model = YOLO("yolov8s.pt") # Other models take longer


script_dir = os.path.dirname(os.path.abspath(__file__))


input_folder = os.path.join(script_dir, 'Camera_7_8_Normal')


output_folder = os.path.join(script_dir, 'Yolo_cam07_08_Powerfull_Model')
os.makedirs(output_folder, exist_ok=True)

for image_filename in os.listdir(input_folder):
    if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, image_filename)
        output_path = os.path.join(output_folder, f"detected_{image_filename}")
        detect_and_save(input_path, output_path, model)
