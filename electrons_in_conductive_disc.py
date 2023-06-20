import numpy as np
import parts_3_4_helper_funcs as hf
import matplotlib.pyplot as plt
import consts

tau = consts.tau_pt_2
q = consts.q

def rand_disc_points(n, r):
    """
    Generate n evenly distributed random points within a 2D disc with radius r.
    Returns a numpy array of shape (n, 2).
    """
    points = np.zeros((n, 2))
    for i in range(n):
        # Generate a random point inside a unit square
        x = np.random.normal()
        y = np.random.normal()
        # Check if the point is inside the disc
        while x ** 2 + y ** 2 > 1:
            x = np.random.normal()
            y = np.random.normal()
        # Scale the point to the desired radius
        scale = r * np.power(np.random.rand(), 1 / 2) / np.sqrt(x ** 2 + y ** 2)
        points[i, 0] = scale * x
        points[i, 1] = scale * y
    return points

def position_after_tau_time(point, r, points):
    a_x, a_y = hf.calculate_electrical_acceleration(point, points)
    new_x = point[0] + 0.5 * (a_x * (tau ** 2))
    new_y = point[1] + 0.5 * (a_y * (tau ** 2))

    # normalize radius when distance is larger than radius of sphere
    distance = np.sqrt(new_x ** 2 + new_y ** 2)
    if distance > r:
        new_x = new_x * (r / distance)
        new_y = new_y * (r / distance)

    return new_x, new_y

def calculate_motion_in_disc(iterations, r, points):
    for iteration in range(iterations):
        new_points = np.copy(points)
        for i, point in enumerate(points):
            x, y = position_after_tau_time(point, r, points)
            new_points[i, 0] = x
            new_points[i, 1] = y
        points = new_points
    return points

def generate_density_by_radius_graph(points,dr, radius, title, show_analytical_graph=False):
    graph = []
    for r in np.arange(0,radius,dr):
        for point in points:
            distance = np.sqrt(point[0] ** 2 + point[1] ** 2)
            if r <= distance < r+dr:
                graph.append(r)
    counts, bins = np.histogram(graph, bins=np.arange(0, radius, dr))

    # Create a figure and axes
    fig, ax1 = plt.subplots()

    # show analytical graph for density
    if (show_analytical_graph):
        r = np.arange(0, radius, 0.05)
        density = 200 * np.abs(q)/(2*np.pi*radius*np.sqrt(radius**2 - r**2))
        ax1.plot(r, density, label='Analytical density')
        ax1.set_ylabel('Analytical density')


    # styling and opening graph
    ax2 = ax1.twinx()
    ax2.hist(bins[:-1], bins, weights=counts, alpha=0.5, label='Numerical Count')
    ax2.set_ylabel('Numerical Count')
    ax1.set_xlabel('Radius')
    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax1.legend(lines + bars, labels + bar_labels)
    plt.title(title)
    plt.show()
