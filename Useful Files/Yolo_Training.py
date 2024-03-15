from ultralytics import YOLO

# Load a pretrained model (recommended for training)
model = YOLO("yolov8s.pt")

# Train the model
model.train(data=r"C:\Users\Barney Evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Maybe\pythonProject1\Overlap-Part-3\Useful Files\dataset.yaml", epochs=100)
