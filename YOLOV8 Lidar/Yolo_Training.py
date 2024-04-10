from ultralytics import YOLO
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def main():
    # Load a pretrained model (recommended for training)
    model = YOLO("yolov8s.pt")

    # Train the model
    model.train(data=r"C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\YOLOV8 Lidar\dataset.yaml", epochs=100)

if __name__ == '__main__':
    main()
