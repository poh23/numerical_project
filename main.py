import electrons_in_conductive_sphere
import electron_in_2d_plane
import electrons_in_conductive_disc
import electrons_in_conductive_square
import parts_3_4_helper_funcs as hf

# Choose Which Part to run
run_part_1 = False
run_part_2 = False
run_part_3 = True
run_part_4 = False
if __name__ == '__main__':
    # part 1 - Drude model -
    if run_part_1:
        num_iterations = 100
        electron_in_2d_plane.calculate_motion(num_iterations)

    # part 2 - Electrons in conductive sphere
    if run_part_2:
        r = 1
        num_electrons = 200
        num_iterations = 150
        # t=0
        points = electrons_in_conductive_sphere.rand_sphere_points_2(num_electrons, r)
        electrons_in_conductive_sphere.create_3d_graph(points, 'Electrons In Sphere at t=0')
        electrons_in_conductive_sphere.generate_density_by_radius_graph(points, r, 'Density by Radius at t=0')
        # t=num_iterations*tau
        new_points, time_graph = electrons_in_conductive_sphere.calculate_motion_in_sphere(num_iterations, r, points)
        electrons_in_conductive_sphere.create_3d_graph(new_points, 'Electrons In Sphere at t={}tau'.format(num_iterations))
        electrons_in_conductive_sphere.show_time_graph(time_graph, 'Electrons In Sphere to on Rim Ratio at t={}tau'.format(num_iterations))
        electrons_in_conductive_sphere.generate_density_by_radius_graph(new_points, r, 'Density by Radius at t={}tau'.format(num_iterations))
        # generate potential graph
        dr = 0.01
        til_radius = 5
        electrons_in_conductive_sphere.find_potential_by_radius(new_points, til_radius, dr)

    # part 3 - Electrons in conductive disc
    if run_part_3:
        r = 1
        num_electrons = 200
        num_iterations = 2000
        dr = 0.05
        # t=0
        points = electrons_in_conductive_disc.rand_disc_points(num_electrons, r)
        hf.plot_points(points, 'Positions in Disc at t=0')
        electrons_in_conductive_disc.generate_density_by_radius_graph(points, dr, r, 'Density by Radius at t=0')
        # t=num_iterations*tau
        new_points = electrons_in_conductive_disc.calculate_motion_in_disc(num_iterations, r, points)
        hf.plot_points(new_points, 'Positions in Disc at t={}tau'.format(num_iterations))
        electrons_in_conductive_disc.generate_density_by_radius_graph(new_points, dr, r,
                                                                      'Density by Radius at t={}tau'.format(
                                                                          num_iterations), True)

    # part 4 - Electrons in conductive square
    if run_part_4:
        r = 1
        num_electrons = 200
        num_iterations = 150
        # t=0
        points = electrons_in_conductive_square.rand_square_points(num_electrons, r)
        hf.plot_points(points, 'Positions in Square at t=0')
        #  t=num_iterations*tau
        new_points = electrons_in_conductive_square.calculate_motion_in_square(num_iterations, r, points)
        hf.plot_points(new_points, 'Positions in Square at t={}tau'.format(num_iterations))
