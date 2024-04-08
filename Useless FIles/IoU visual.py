import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_iou_with_close_iou_text(box_a, box_b):
    """
    Plots two centered overlapping boxes to demonstrate the Intersection over Union (IoU), with boxes of the same size,
    highlighting the non-overlapping sectors with corresponding colors. Adjusts the IoU value to be closer beneath the figure
    with a smaller font, and places the labels for ground truth and prediction appropriately. The plot size is increased.

    :param box_a: The first bounding box [x, y, width, height] representing the ground truth
    :param box_b: The second bounding box [x, y, width, height] representing the prediction
    """
    fig, ax = plt.subplots(figsize=(10, 8))  # Increase the figure size

    # Create the rectangles representing each box with highlighted non-overlapping sectors
    rect_a = patches.Rectangle((box_a[0], box_a[1]), box_a[2], box_a[3], linewidth=2, edgecolor='blue',
                               facecolor='blue', alpha=0.2)
    rect_b = patches.Rectangle((box_b[0], box_b[1]), box_b[2], box_b[3], linewidth=2, edgecolor='red', facecolor='red',
                               alpha=0.2)

    # Add the rectangles to the Axes
    ax.add_patch(rect_a)
    ax.add_patch(rect_b)

    # Add labels for the rectangles, with adjusted positions and font properties
    ax.text(box_a[0] + box_a[2] / 2, box_a[1] - 0.2, 'Ground Truth', color='black', ha='center', va='center',
            fontsize=11, style='italic')
    ax.text(box_b[0] + box_b[2] / 2, box_b[1] + box_b[3] + 0.2, 'Prediction', color='black', ha='center', va='center',
            fontsize=11, style='italic')

    # Calculate the intersection and union areas
    dx = min(box_a[0] + box_a[2], box_b[0] + box_b[2]) - max(box_a[0], box_b[0])
    dy = min(box_a[1] + box_a[3], box_b[1] + box_b[3]) - max(box_a[1], box_b[1])
    intersection_area = dx * dy if (dx >= 0) and (dy >= 0) else 0
    union_area = box_a[2] * box_a[3] + box_b[2] * box_b[3] - intersection_area

    # Calculate the IoU
    iou = intersection_area / union_area if union_area != 0 else 0

    # Hide the axes and adjust plot area
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')

    # Add a new text box for the IoU value closer to the boxes
    text_box = patches.FancyBboxPatch((5, 5.5), 1.8, 0.6, boxstyle="round,pad=0.1", ec="none", fc="white", lw=2)
    ax.add_patch(text_box)
    ax.text(5.9, 5.8, f'IoU: {iou:.2f}', verticalalignment='center', horizontalalignment='center', color='black',
            fontsize=15, style='italic')

    plt.show()


# Example coordinates for the bounding boxes
box_a = [1, 1, 6, 6]
box_b = [3, 3, 6, 6]
box_a = [x + 0.3 for x in box_a]
box_b = [x - 0.3 for x in box_b]
box_a = [2, 2, 6, 6]
box_b = [4, 4, 6, 6]

plot_iou_with_close_iou_text(box_a, box_b)
