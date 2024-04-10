from ultralytics import YOLO
import os
import torch

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def main():
    # Load a pretrained model (recommended for training)
    model = YOLO("yolov8s.pt")

    # Check for GPU availability and use it if possible
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    print(f"Training on device: {device}")

    # Train the model with more options
    model.train(
        data=r"C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Actual_Yolo_Train\dataset.yaml",
        epochs=100,
        batch_size=16,
    )

    # Save the trained model
    model_path = r"C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Actual_Yolo_Train\trained_model.pt"
    model.save(model_path)
    print(f"Trained model saved to {model_path}")

if __name__ == '__main__':
    main()
