import matplotlib.pyplot as plt
import numpy as np


def convert_angle_to_radians(angle):
    """Convert an angle in degrees to radians."""
    return np.deg2rad(angle)


def generate_arc(center, radius, angle_start, angle_end, steps=100):
    """Generate the x and y coordinates for an arc."""
    theta = np.linspace(angle_start, angle_end, steps)
    return center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta)


def draw_sector(ax, center, radius, angle_start, angle_end, rotation_angle=0, color='blue', alpha=0.3):
    """Draw a sector given the center, radius, and angle range."""
    # Generate arc
    arc_x, arc_y = generate_arc(center, radius, angle_start, angle_end)

    # Rotate arc if needed
    if rotation_angle != 0:
        arc_x, arc_y = rotate_sector(arc_x, arc_y, center, rotation_angle)

    # Draw sector
    sector = np.concatenate(([center], np.column_stack((arc_x, arc_y)), [center]))
    ax.fill(sector[:, 0], sector[:, 1], color=color, alpha=alpha)


def rotate_sector(arc_x, arc_y, center, rotation_angle):
    """Rotate the arc around the center by the rotation angle."""
    rotated_x = (arc_x - center[0]) * np.cos(rotation_angle) - (arc_y - center[1]) * np.sin(rotation_angle) + center[0]
    rotated_y = (arc_x - center[0]) * np.sin(rotation_angle) + (arc_y - center[1]) * np.cos(rotation_angle) + center[1]
    return rotated_x, rotated_y


def main():
    # Define the parameters for the sectors
    radius = 10
    angle = 120  # in degrees
    center_1 = (0, 0)
    center_2 = (3, 0)
    rotation_angle1 = convert_angle_to_radians(0)  # Rotate by 45 degrees
    rotation_angle2 = convert_angle_to_radians(-9)

    # Plot setup
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

    # Draw and rotate the first sector
    draw_sector(ax, center_1, radius, 0, convert_angle_to_radians(angle), rotation_angle1, color='blue')

    # Draw and rotate the second sector
    draw_sector(ax, center_2, radius, np.pi - convert_angle_to_radians(angle), np.pi, rotation_angle2, color='red')

    # Final plot adjustments
    #ax.set_xlim(-150, 150)
    #ax.set_ylim(-150, 150)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()
