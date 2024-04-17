import numpy as np
from skspatial.objects import Plane, Point, Vector

# Your provided frustum corners
frustum_corners1 = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

frustum_corners2 = np.array([
    [0.5, 0.5, -0.5],
    [1.5, 0.5, -0.5],
    [1.5, 1.5, -0.5],
    [0.5, 1.5, -0.5],
    [0.5, 0.5, 0.5],
    [1.5, 0.5, 0.5],
    [1.5, 1.5, 0.5],
    [0.5, 1.5, 0.5]
])

faces = [
        [0, 1, 2, 3],  # bottom face
        [4, 5, 6, 7],  # top face
        [0, 1, 5, 4],  # side face
        [1, 2, 6, 5],  # side face
        [2, 3, 7, 6],  # side face
        [3, 0, 4, 7]   # side face
    ]

def calculate_plane_equation(frustum_corners):
    faces = [
        [0, 1, 2, 3],  # bottom face
        [4, 5, 6, 7],  # top face
        [0, 1, 5, 4],  # side face
        [1, 2, 6, 5],  # side face
        [2, 3, 7, 6],  # side face
        [3, 0, 4, 7]   # side face
    ]

    plane_equations = []
    for face in faces:
        p1, p2, p3 = frustum_corners[face[:3]]
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        D = -np.dot(normal, p1)
        plane_equations.append(np.append(normal, D))

    return plane_equations

# Calculate plane equations for each frustum
planes1 = calculate_plane_equation(frustum_corners1)
planes2 = calculate_plane_equation(frustum_corners2)

# Creating Plane objects from the calculated plane equations
sk_planes1 = [Plane(point=frustum_corners1[face[0]], normal=eq[:3]) for face, eq in zip(faces, planes1)]
sk_planes2 = [Plane(point=frustum_corners2[face[0]], normal=eq[:3]) for face, eq in zip(faces, planes2)]

# Example output of Plane objects
for i, plane in enumerate(sk_planes1):
    print(f"Plane {i} from Frustum 1: {plane}")

for i, plane in enumerate(sk_planes2):
    print(f"Plane {i} from Frustum 2: {plane}")
