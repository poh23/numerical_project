import numpy as np
import matplotlib.pyplot as plt
import consts

k = consts.k
q = consts.q
mass = consts.mass
tau = consts.tau_pt_2

def plot_points(points, title):
    """
    Plot the given points using Matplotlib.
    points: numpy array of shape (n, 2) representing (x, y) coordinates.
    """
    x = points[:, 0]  # Extract x-coordinates from points
    y = points[:, 1]  # Extract y-coordinates from points

    plt.scatter(x, y)  # Plot the points
    plt.axis('equal')  # Set equal aspect ratio for x and y axes
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.grid(True)
    plt.show()

def calculate_electrical_acceleration(point, points):
    sum_force_x = 0
    sum_force_y = 0
    for i in points:
        x = point[0] - i[0]
        y = point[1] - i[1]
        r_tripled = np.power(x ** 2 + y ** 2 , 3 / 2)
        if r_tripled != 0:
            sum_force_x += k * q * q * x / r_tripled
            sum_force_y += k * q * q * y / r_tripled
    a_x, a_y = sum_force_x / mass, sum_force_y / mass
    return a_x, a_y
