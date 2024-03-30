from PIL import Image, ImageDraw
from Maximum_Overlap import area_percentage


def apply_gradient_overlay(image, overlap_percent, side, start_opacity=255, end_opacity=0):
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


def create_highlighted_images(first_image_path, second_image_path, overlap_percent):
    # Load images
    first_image = Image.open(first_image_path).convert('RGBA')
    second_image = Image.open(second_image_path).convert('RGBA')

    # Apply the gradient overlay to the right side of the first image
    first_image_with_highlight = apply_gradient_overlay(first_image, overlap_percent, 'right', start_opacity=64)
    # Apply the gradient overlay to the left side of the second image
    second_image_with_highlight = apply_gradient_overlay(second_image, overlap_percent, 'left', start_opacity=64)

    # Save or display the images
    first_image_with_highlight.show()
    second_image_with_highlight.show()


# Paths relative to the script location
first_image_path = "../Images/cam07.jpg"
second_image_path = "../Images/cam08.jpg"

# Example usage with a 20% overlap
create_highlighted_images(first_image_path, second_image_path, area_percentage)