import numpy as np
import parts_3_4_helper_funcs as hf
import consts

tau = consts.tau_pt_2

def rand_square_points(n, r):
    """
    Generate n evenly distributed random points within a 2D square with side length of 2r.
    Returns a numpy array of shape (n, 2).
    """
    points = np.zeros((n, 2))
    for i in range(n):
        # Generate a random point inside a unit square
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        # Check if the point is inside the square
        while x > 1 or x < -1 or y > 1 or y < -1:
            x = np.random.uniform(-1, 1)
            y = np.random.uniform(-1, 1)
        # Scale the point to the desired length
        points[i, 0] = r * x
        points[i, 1] = r * y
    return points

def position_after_tau_time(point, r, points):
    a_x, a_y = hf.calculate_electrical_acceleration(point, points)
    new_x = point[0] + 0.5 * (a_x * (tau ** 2))
    new_y = point[1] + 0.5 * (a_y * (tau ** 2))

    # normalize x,y values when they're larger than length of square
    if new_x > r or new_x < -r:
        new_x = new_x * (r / np.abs(new_x))
    if new_y > r or new_y < -r:
        new_y = new_y * (r / np.abs(new_y))

    return new_x, new_y

def calculate_motion_in_square(iterations, r, points):
    '''

    :param iterations:
    :param r:
    :param points:
    :return: main function which simulate the electrons motion in square
    '''
    for iteration in range(iterations):
        new_points = np.copy(points)
        for i, point in enumerate(points):
            x, y = position_after_tau_time(point, r, points)
            new_points[i, 0] = x
            new_points[i, 1] = y
        points = new_points
    return points