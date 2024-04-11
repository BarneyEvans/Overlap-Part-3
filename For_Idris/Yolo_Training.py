from ultralytics import YOLO
import torch

def main():
    # Load a pretrained model (recommended for training)
    model = YOLO("yolov8s.pt")

    # Check for GPU availability and use it if possible
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    print(f"Training on device: {device}")

    # Define the dataset configuration and model save path relative to the home directory
    home_dir = '/lyceum/be1g21/V6'
    data_config_path = f'{home_dir}/dataset/dataset.yaml'
    model_save_path = f'{home_dir}/trained_model.pt'

    # Train the model with more options
    model.train(
        data=data_config_path,
        epochs=100,
    )

    # Save the trained model
    model.save(model_save_path)
    print(f"Trained model saved to {model_save_path}")

if __name__ == '__main__':
    main()
