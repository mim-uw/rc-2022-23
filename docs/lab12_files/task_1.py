import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import sys

def plot_plot(case = 1):

    fig = plt.figure(figsize=[10, 8])
    ax  = fig.add_subplot(1, 1, 1, projection='3d')

    matrix_1 = [
            [1, 0, 0, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

    matrix_2 = [
            [1, 0, 0, -2],
            [0, 1, 0, 2],
            [0, 0, 1, 1],
            [0, 0, 0, 1]]

    matrix_5 = np.zeros((4, 4))
    matrix_5[:3, :3] = R.from_euler('z', 90, degrees=True).as_matrix()
    matrix_5[3, 3] = 1
    matrix_6 = np.zeros((4, 4))
    matrix_6[:3, :3] = R.from_euler('z', 90, degrees=True).inv().as_matrix()
    matrix_6[3, 3] = 1

    def plot_matrix(transformation_matrix):
        for v, c in zip([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]], ['r', 'g', 'b']):
            zero = [0, 0, 0, 1]
            x, y, z, _ = zip(zero, v)
            plt.plot(x, y, z, f'--{c}', linewidth=1)
            x, y, z, _ = zip(np.dot(transformation_matrix, zero), np.dot(transformation_matrix, v))
            plt.plot(x, y, z, f'-{c}', linewidth=1)


    if case == 1: plot_matrix(matrix_1)
            
    if case == 2: plot_matrix(matrix_2)


    # Are those two equal?
    if case == 3: plot_matrix(np.dot(matrix_1, matrix_2))
    if case == 4: plot_matrix(np.dot(matrix_2, matrix_1))

    if case == 5: plot_matrix(matrix_5)
            
    if case == 6: plot_matrix(matrix_6)

    # Are those two equal?
    if case == 7: plot_matrix(np.dot(matrix_5, matrix_1))
    if case == 8: plot_matrix(np.dot(matrix_2, matrix_5))

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)

    plt.show()

# For every single one of eight cases, without looking at the source code, just by looking at
# plots, find a matrix

if __name__ == '__main__':
    plot_plot(int(sys.argv[1]))