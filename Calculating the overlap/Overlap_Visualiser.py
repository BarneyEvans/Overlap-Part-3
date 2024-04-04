from PIL import Image, ImageDraw
from Maximum_Overlap import area_percentage
import os

def apply_gradient_overlay(image, overlap_percent, side, start_opacity=125, end_opacity=125):
    # Calculate the width of the overlap region
    width, height = image.size
    overlap_width = int(width * overlap_percent)

    # Create an alpha mask for the gradient
    alpha_mask = Image.new('L', (overlap_width, height), color=0)
    draw = ImageDraw.Draw(alpha_mask)

    # Draw the gradient on the alpha mask
    for x in range(overlap_width):
        # Calculate the opacity for this column of pixels
        if side == 'right':
            opacity = int(start_opacity + (end_opacity - start_opacity) * x / overlap_width)
        else:  # side == 'left'
            opacity = int(end_opacity + (start_opacity - end_opacity) * x / overlap_width)
        draw.line((x, 0, x, height), fill=opacity)

    # Create a solid yellow image for the overlay
    yellow = Image.new('RGBA', (overlap_width, height), (255, 255, 0, 255))

    # Apply the alpha mask to the yellow overlay
    yellow.putalpha(alpha_mask)

    # Paste the yellow overlay onto the original image
    if side == 'right':
        image.paste(yellow, (width - overlap_width, 0), yellow)
    else:  # side == 'left'
        image.paste(yellow, (0, 0), yellow)

    return image


def create_highlighted_images(first_image_path, second_image_path, overlap_percent, output_dir):
    # Load images
    first_image = Image.open(first_image_path)
    second_image = Image.open(second_image_path)

    # Apply the gradient overlay to the right side of the first image
    first_image_with_highlight = apply_gradient_overlay(first_image, overlap_percent, 'right', start_opacity=64)
    # Apply the gradient overlay to the left side of the second image
    second_image_with_highlight = apply_gradient_overlay(second_image, overlap_percent, 'left', start_opacity=64)

    # Save the images with new file names in the output directory
    first_image_name = os.path.basename(first_image_path)
    second_image_name = os.path.basename(second_image_path)

    first_image_with_highlight.save(os.path.join(output_dir, first_image_name.replace('.jpg', '_with_highlight.jpg')))
    second_image_with_highlight.save(os.path.join(output_dir, second_image_name.replace('.jpg', '_with_highlight.jpg')))


output_dir = "../Images/Undistorted_Images/Undistored_Images_Overlap"

# Paths relative to the script location
first_image_path = "../Images/Undistorted_Images/cam07.jpg"
second_image_path = "../Images/Undistorted_Images/cam08.jpg"

# Example usage with a 20% overlap
create_highlighted_images(first_image_path, second_image_path, area_percentage, output_dir)