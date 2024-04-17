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

def main():
    # Define corners for the frustums
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

    plot_two_frustums(frustum_corners1, frustum_corners2)
    faces = define_frustum_faces()

    # Compute plane equations for both frustums
    planes1 = compute_all_plane_equations(frustum_corners1, faces)
    planes2 = compute_all_plane_equations(frustum_corners2, faces)

    print(planes1)

    # Prepare to plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the intersection lines between the frustums
    for p1 in planes1:
        for p2 in planes2:
            try:
                U, C = get_plane_plane_intersection(p1, p2)
                t = np.linspace(-1, 1, 100)
                line_points = C[:, np.newaxis] + U[:, np.newaxis] * t
                ax.plot(line_points[0], line_points[1], line_points[2], 'r-')
            except np.linalg.LinAlgError:
                continue

    # Setting the labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Intersection of Two Frustums')
    plt.show()

# Call the main function
main()
