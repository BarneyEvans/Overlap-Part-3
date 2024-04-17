import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Plot_Frustrum import plot_two_frustums

def compute_plane_equation(p1, p2, p3):
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p3) - np.array(p1)
    normal = np.cross(v1, v2)
    if np.linalg.norm(normal) == 0:
        return None
    normal = normal / np.linalg.norm(normal)
    D = -np.dot(normal, np.array(p1))
    return normal[0], normal[1], normal[2], D

def compute_all_plane_equations(frustum_corners, faces):
    plane_equations = []
    for face in faces:
        if len(face) < 3:
            continue
        p1, p2, p3 = frustum_corners[face[0]], frustum_corners[face[1]], frustum_corners[face[2]]
        plane_eq = compute_plane_equation(p1, p2, p3)
        if plane_eq:
            plane_equations.append(plane_eq)
    return plane_equations

def normalized(X):
    return X / np.linalg.norm(X)

def get_plane_plane_intersection(A, B):
    U = normalized(np.cross(A[:-1], B[:-1]))
    M = np.array((A[:-1], B[:-1], U))
    X = np.array((-A[-1], -B[-1], 0.))
    return U, np.linalg.solve(M, X)

def define_frustum_faces():
    return [
        [0, 1, 2, 3],  # bottom face
        [4, 5, 6, 7],  # top face
        [0, 1, 5, 4],  # side face
        [1, 2, 6, 5],  # side face
        [2, 3, 7, 6],  # side face
        [3, 0, 4, 7]   # side face
    ]

def define_frustum_edges(frustum_corners):
    return [
        [0, 1], [1, 2], [2, 3], [3, 0],  # lower square
        [4, 5], [5, 6], [6, 7], [7, 4],  # upper square
        [0, 4], [1, 5], [2, 6], [3, 7]   # vertical lines
    ]


def line_plane_intersection(plane, p0, p1):
    # plane is defined as (A, B, C, D)
    # Line segment is defined by two points p0 and p1
    point = np.array(p0)
    direction = np.array(p1) - np.array(p0)
    denominator = np.dot(plane[:3], direction)

    if np.abs(denominator) < 1e-6:
        # Line and plane are parallel
        return None

    t = -(np.dot(plane[:3], point) + plane[3]) / denominator
    intersection = point + t * direction

    if 0 <= t <= 1:  # The intersection lies within the line segment
        return intersection
    else:
        return None


def main():
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

    faces = define_frustum_faces()

    planes1 = compute_all_plane_equations(frustum_corners1, faces)
    planes2 = compute_all_plane_equations(frustum_corners2, faces)

    edges1 = define_frustum_edges(frustum_corners1)
    edges2 = define_frustum_edges(frustum_corners2)

    intersection_points = []

    # Find intersections for edges from frustum1 with planes from frustum2
    for edge_indices in edges1:
        p0, p1 = frustum_corners1[edge_indices[0]], frustum_corners1[edge_indices[1]]
        for plane in planes2:
            intersection = line_plane_intersection(plane, p0, p1)
            if intersection is not None:
                intersection_points.append(intersection)

    # Find intersections for edges from frustum2 with planes from frustum1
    for edge_indices in edges2:
        p0, p1 = frustum_corners2[edge_indices[0]], frustum_corners2[edge_indices[1]]
        for plane in planes1:
            intersection = line_plane_intersection(plane, p0, p1)
            if intersection is not None:
                intersection_points.append(intersection)

    # Prepare to plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the intersection points
    for point in intersection_points:
        ax.scatter(*point, color='r')

    # Plot the edges of frustums for reference
    for edge in edges1:
        ax.plot3D(*zip(frustum_corners1[edge[0]], frustum_corners1[edge[1]]), color='b')
    for edge in edges2:
        ax.plot3D(*zip(frustum_corners2[edge[0]], frustum_corners2[edge[1]]), color='g')

    # Setting the labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Intersection Points of Two Frustums')
    plt.show()

# Call the main function
main()
