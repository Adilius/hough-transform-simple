import numpy as np
import matplotlib.pyplot as plt

# Returns a list of tuples representing points
def read_input(file_name: str):

    with open(file_name, 'r') as input_file:
        point_list = input_file.read().split('\n')
        x_coords = []
        y_coords = []
        for point in point_list:
            x_string, y_string = point.split(',')
            x_coords.append(float(x_string))
            y_coords.append(float(y_string))
    
    return x_coords, y_coords

# Calculate hough space
def calculate_hough_space(x_coords, y_coords):

    # Rho and Theta ranges
    thetas = np.deg2rad(np.arange(-90, 90))
    rhos = []
    for x, y  in zip(x_coords,y_coords):
        line_list = []
        for theta in thetas:

            # Hesse normal form
            r = x * np.cos(theta) + y * np.sin(theta)
            line_list.append(r)
        rhos.append(line_list)

    rhos = np.asarray(rhos)

    return thetas, rhos

# Get cross line between two points
def get_cross_line(x, y, theta):
    index = np.argwhere(np.diff(np.sign(x - y)) != 0)
    theta = theta[index]
    rho = x[index]
    x_list = np.arange(start=0, stop=7, step=0.5)
    y_list = np.zeros(len(x_list))
    for i, x in enumerate(x_list):
        y_list[i] = ((-np.cos(theta)/np.sin(theta))*x) +  (rho/np.sin(theta))

    return x_list, y_list

# Display hough space
def show_hough_space(x_list_list, y_list_list, x_coords, y_coords, thetas, rhos):
    fig , (ax1, ax2) = plt.subplots(1,2)
    
    # Cartesian space dots
    ax1.scatter(x_coords, y_coords)

    # Cartesian space lines
    for i in range(len(x_list_list)):
        ax1.plot(x_list_list[i], y_list_list[i])
    
    # Hough space graph
    for rho in rhos:
        ax2.plot(thetas, rho)
    plt.show()

if __name__ == '__main__':
    # Read coordinates from input file
    x_coords, y_coords = read_input('input_points.txt')

    # Calculate thetas and rhos
    thetas, rhos = calculate_hough_space(x_coords, y_coords)

    # Get cross lines
    x_list_list = []
    y_list_list = []
    for first_point in range(len(x_coords)-1):
        for second_point in range(first_point+1, len(x_coords)):
            x_list, y_list = get_cross_line(rhos[first_point], rhos[second_point], thetas)
            x_list_list.append(x_list)
            y_list_list.append(y_list)

    # Plot cartesian space and hough space
    show_hough_space(x_list_list, y_list_list, x_coords, y_coords, thetas, rhos)