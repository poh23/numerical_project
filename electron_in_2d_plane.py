# This is a sample Python script.
import random
import math
import consts
import numpy as np
import matplotlib.pyplot as plt

mass = consts.mass
q = consts.q
E = consts.E
t_0 = consts.t_0
tau = consts.tau
init_v = consts.init_v


def position_after_tau_time(x, y, v_x, v_y):
    a = (E * q) / mass
    new_x = x + v_x * tau + 0.5 * (a * (tau ** 2))
    new_y = y + v_y * tau
    return new_x, new_y


def generate_random_v():
    rand_angle = 2 * math.pi * random.random()
    v_x = init_v * math.cos(rand_angle)
    v_y = init_v * math.sin(rand_angle)
    return v_x, v_y


def calculate_motion(num_taus):
    x_positions = [0]
    y_positions = [0]
    for i in range(0, num_taus):
        v_x, v_y = generate_random_v()
        new_pos_x, new_pos_y = position_after_tau_time(x_positions[i], y_positions[i], v_x, v_y)
        x_positions.append(new_pos_x)
        y_positions.append(new_pos_y)
    show_graph(x_positions, y_positions, num_taus)


def calculate_avg_velocity(x_pos, y_pos, num_taus):
    delta_x = x_pos[-1] - x_pos[0]
    delta_y = y_pos[-1] - y_pos[0]
    total_time = t_0 + num_taus * tau
    avg_velocity_x, avg_velocity_y = delta_x / total_time, delta_y / total_time
    return avg_velocity_x, avg_velocity_y


def show_graph(x_positions, y_positions, num_taus):
    avg_velocity = calculate_avg_velocity(x_positions, y_positions, num_taus)
    fig, ax = plt.subplots()

    xpoints = np.array(x_positions)
    ypoints = np.array(y_positions)
    ax.plot(xpoints, ypoints)
    plt.title('Position of electron by time')
    plt.xlabel("X Position")
    plt.ylabel("Y Position")

    # show on graph average velocity
    ax.annotate('Average Velocity in- \nx axis: {} \ny axis: {}'.format(np.round(avg_velocity[0], 4),
                                                                        np.round(avg_velocity[1], 4)),
                xy=(1, 0), xycoords='axes fraction',
                xytext=(-100, 20), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='bottom')
    plt.show()
