import numpy as np


# The given code function with slight adjustments for safety and accuracy
def calculate_circular_segment_area(x1, y1, x2, y2, radius):
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")

    # Calculate the chord length c
    c = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    if c > 2 * radius:
        raise ValueError("The chord length cannot be greater than the diameter of the circle.")

    # Ensure the argument of arccos is within the domain
    cos_theta_half = np.clip(c / (2 * radius), -1, 1)

    # Calculate the central angle theta for the segment in radians
    theta = 2 * np.arccos(cos_theta_half)

    # Calculate the height h' from the chord to the arc
    h_prime = radius - np.sqrt(radius ** 2 - (c / 2) ** 2)

    # Calculate the area of the circular segment
    area_sector = (theta / (2 * np.pi)) * (np.pi * radius ** 2)
    area_triangle = (c * (radius - h_prime)) / 2
    area_segment = area_sector - area_triangle

    return area_segment


# A test run of the function with hypothetical coordinates and radius
# For testing purposes, let's assume some coordinates and radius
test_x1, test_y1 = (50.7331221513823, 87.8723451927921)  # Coordinate 1
test_x2, test_y2 = (1.5, 99.9887)  # Coordinate 2
test_radius = 100  # Radius of the circle

# Running the test function
try:
    result = calculate_circular_segment_area(test_x1, test_y1, test_x2, test_y2, test_radius)
except ValueError as e:
    result = str(e)

print(result)
