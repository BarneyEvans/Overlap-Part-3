from ultralytics import YOLO
import os

# Setting the environment variable to avoid potential OpenMP runtime error
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def detect_and_visualize(model, image_paths):
    # Run inference on a batch of images
    results = model(image_paths)

    # Process results for each image
    for result in results:
        # Display to screen
        result.show()


def main():
    # Load the trained model
    model_path = r"C:\Users\be1g21\PycharmProjects\pythonProject3\Overlap-Part-3\Useful Files\runs\detect\train9\weights\best.pt"
    model = YOLO(model_path)

    # Specify the directory containing images you want to process
    image_dir = r"C:\Users\be1g21\PycharmProjects\pythonProject3\Overlap-Part-3\Images"
    images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('png', 'jpg', 'jpeg'))]

    # Detect and visualize for the batch of images
    detect_and_visualize(model, images)

if __name__ == '__main__':
    main()
