import numpy as np
from skspatial.objects import Plane
from skspatial.plotting import plot_3d

class PlaneWithCorners():
    def __init__(self, corners):
        self.corners = corners
        self.normalize_normal_vector()

    def normalize_normal_vector(self):
        # Calculate two vectors from the corners
        vector1 = self.corners[1] - self.corners[0]
        vector2 = self.corners[2] - self.corners[0]
        # Calculate the normal vector to the plane using the cross product
        normal_vector = np.cross(vector1, vector2)
        # Normalize the normal vector
        normalized_normal_vector = normal_vector / np.linalg.norm(normal_vector)
        self.normal_vector = normalized_normal_vector

# Define a function to extract coordinates defining each plane
def extract_plane_coordinates(corners):
    # Near Plane: corners 0, 1, 2, and 3
    near_plane = [corners[0], corners[1], corners[2], corners[3]]
    # Far Plane: corners 4, 5, 6, and 7
    far_plane = [corners[4], corners[5], corners[6], corners[7]]
    # Left Plane: corners 0, 4, 7, and 3
    left_plane = [corners[0], corners[4], corners[7], corners[3]]
    # Right Plane: corners 1, 5, 6, and 2
    right_plane = [corners[1], corners[5], corners[6], corners[2]]
    # Top Plane: corners 0, 1, 5, and 4
    top_plane = [corners[0], corners[1], corners[5], corners[4]]
    # Bottom Plane: corners 3, 2, 6, and 7
    bottom_plane = [corners[3], corners[2], corners[6], corners[7]]

    return {
        "Near Plane": near_plane,
        "Far Plane": far_plane,
        "Left Plane": left_plane,
        "Right Plane": right_plane,
        "Top Plane": top_plane,
        "Bottom Plane": bottom_plane
    }

# Define the corners of the plane
corners = np.array([
    [-0.14184547,  0.07535541, -0.1],
    [ 0.14184547,  0.07535541, -0.1],
    [ 0.14184547, -0.07535541, -0.1],
    [-0.14184547, -0.07535541, -0.1],
    [-141.84546825,  75.35540501, -100.],
    [ 141.84546825,  75.35540501, -100.],
    [ 141.84546825, -75.35540501, -100.],
    [-141.84546825, -75.35540501, -100.]
])

# Create a PlaneWithCorners object for each plane
planes = {}
for plane, corners in extract_plane_coordinates(corners).items():
    planes[plane] = PlaneWithCorners(corners)


actual_planes = []
# Print the normal vectors for each plane
for plane, plane_obj in planes.items():
    print(plane + ":")
    print("  Normal Vector:", plane_obj.normal_vector)
    print("  Corners:", plane_obj.corners[0])
    actual_planes.append(Plane(plane_obj.corners[0], plane_obj.normal_vector))

print(len(actual_planes))

plot_3d(
    *[plane.plotter(alpha=0.5) for plane in actual_planes]
)

