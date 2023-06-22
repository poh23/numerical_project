import numpy as np
import consts
import matplotlib.pyplot as plt

k = consts.k
q = consts.q
mass = consts.mass
tau = consts.tau_pt_2
r_resolution = 0.01
places_after_point = int(np.abs(np.log10(r_resolution)))


def rand_sphere_points_2(n, r):
    """
    Generate n evenly distributed random points within a 3D sphere with radius r.
    Returns a numpy array of shape (n, 3).
    """
    points = np.zeros((n, 3))
    for i in range(n):
        # Generate a random point inside a unit cube
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        z = np.random.uniform(-1, 1)
        # Check if the point is inside the sphere
        while x ** 2 + y ** 2 + z ** 2 > 1:
            x = np.random.uniform(-1, 1)
            y = np.random.uniform(-1, 1)
            z = np.random.uniform(-1, 1)
        # Scale the point to the desired radius
        scale = r * np.power(np.random.uniform(0, 1), 1 / 3) / np.sqrt(x ** 2 + y ** 2 + z ** 2)
        points[i, 0] = scale * x
        points[i, 1] = scale * y
        points[i, 2] = scale * z
    return points


def calculate_electrical_acceleration(point, points):
    sum_force_x = 0
    sum_force_y = 0
    sum_force_z = 0
    for i in points:
        x = point[0] - i[0]
        y = point[1] - i[1]
        z = point[2] - i[2]
        r_tripled = np.power(x ** 2 + y ** 2 + z ** 2, 3 / 2)
        if r_tripled != 0:
            sum_force_x += k * q * q * x / r_tripled
            sum_force_y += k * q * q * y / r_tripled
            sum_force_z += k * q * q * z / r_tripled
    a_x, a_y, a_z = sum_force_x / mass, sum_force_y / mass, sum_force_z / mass
    return a_x, a_y, a_z


def calculate_motion_in_sphere(iterations, r, points):
    '''

    :param iterations:
    :param r:
    :param points:
    :return: main function which simulates the motion of the electrons in sphere and returns new position of electrons and Percentage Of Electrons in Sphere data for graph
    '''
    time = 0
    time_graph = np.zeros((iterations, 2))
    for iteration in range(iterations):
        new_points = np.copy(points)
        for i, point in enumerate(points):
            x, y, z = position_after_tau_time(point, r, points)
            new_points[i, 0] = x
            new_points[i, 1] = y
            new_points[i, 2] = z
        points = new_points
        # gather data about the percentage of electrons in the sphere after each iteration
        time += tau
        time_graph[iteration, 0] = time
        time_graph[iteration, 1] = find_percentage_of_electrons_in_sphere(points, r)
    return points, time_graph


def position_after_tau_time(point, r, points):
    a_x, a_y, a_z = calculate_electrical_acceleration(point, points)
    new_x = point[0] + 0.5 * (a_x * (tau ** 2))
    new_y = point[1] + 0.5 * (a_y * (tau ** 2))
    new_z = point[2] + 0.5 * (a_z * (tau ** 2))

    # normalize radius when distance is larger than radius of sphere
    distance = np.sqrt(new_x ** 2 + new_y ** 2 + new_z ** 2)
    if distance > r:
        new_x = new_x * (r / distance)
        new_y = new_y * (r / distance)
        new_z = new_z * (r / distance)

    return new_x, new_y, new_z


def generate_density_by_radius_graph(points, r, title):
    graph = []
    for i, point in enumerate(points):
        graph.append(np.round(np.sqrt(point[0] ** 2 + point[1] ** 2 + point[2] ** 2), places_after_point))
    counts, bins = np.histogram(graph, bins=np.arange(0, r + r_resolution, r_resolution))
    plt.figure(figsize=(14, 6))
    plt.hist(bins[:-1], bins, weights=counts)

    # styling and opening graph
    plt.title(title)
    plt.xlabel("Radius")
    plt.ylabel("Count")
    plt.show()


def find_percentage_of_electrons_in_sphere(points, r):
    points_in_sphere = 0
    for point in points:
        if np.sqrt(point[0] ** 2 + point[1] ** 2 + point[2] ** 2) < r - r_resolution:
            points_in_sphere += 1

    return points_in_sphere / len(points)


def show_time_graph(time_graph, title):
    plt.plot(time_graph[:, 0], time_graph[:, 1])
    # styling and opening graph
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Percentage Of Electrons in Sphere (not on the rim)")
    plt.show()

def create_3d_graph(points, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2])
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_title(title)
    plt.show()

def find_potential_by_radius(points, radius, dr):
    potential_by_r = []
    for r in np.arange (0, radius, dr):
        # find average potential of 6 sample points with same radius
        potential_in_x_dr = calculate_potential_in_point([r, 0, 0], points)
        potential_in_y_dr = calculate_potential_in_point([0, r, 0], points)
        potential_in_z_dr = calculate_potential_in_point([0, 0, r], points)
        potential_in_minus_x_dr = calculate_potential_in_point([-r, 0, 0], points)
        potential_in_minus_y_dr = calculate_potential_in_point([0, -r, 0], points)
        potential_in_minus_z_dr = calculate_potential_in_point([0, 0, -r], points)
        avg_potential_in_dr = (potential_in_x_dr + potential_in_y_dr + potential_in_z_dr + potential_in_minus_x_dr + potential_in_minus_y_dr + potential_in_minus_z_dr)/6
        potential_by_r.append([r, avg_potential_in_dr])

    graph = np.array(potential_by_r)
    plt.plot(graph[:, 0], graph[:, 1])
    # styling and opening graph
    plt.title('Potential By R')
    plt.xlabel("Radius")
    plt.ylabel("Potential")
    plt.show()


def calculate_potential_in_point(point, points):
    # sums the potentials which each electron creates
    sum_potential = 0
    for i in points:
        x = point[0] - i[0]
        y = point[1] - i[1]
        z = point[2] - i[2]
        r_tripled = np.power(x ** 2 + y ** 2 + z ** 2, 1 / 2)
        if r_tripled != 0:
            sum_potential += k * q / r_tripled
    return sum_potential






