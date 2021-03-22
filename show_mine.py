import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


# method to show maze in the form of an image for easier visualization
def show(mine):
    """
    Method that uses PyPlot to plot the maze on an image to make it easier to see if it was solved and the route to goal
    :param mine: mine to be plotted
    :return: void
    """
    temp_mine = np.zeros((len(mine), len(mine)))
    for i in range(len(mine)):
        for j in range(len(mine)):
            if mine[i][j].hidden:
                temp_mine[i][j] = -2
            elif mine[i][j].flag:
                temp_mine[i][j] = -3
            elif mine[i][j].value == 1:
                temp_mine[i][j] = -1
            else:
                temp_mine[i][j] = mine[i][j].clue

    # make color map of fixed colors
    cmap = colors.ListedColormap(['yellow', 'grey', 'tab:red', 'white'])
    bounds = [-3, -2, -1, 0, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # have imshow show only colors specified on the inputs specified
    plt.imshow(temp_mine, interpolation='none', cmap=cmap, norm=norm)
    plt.grid()
    ax = plt.gca()
    ax.set_yticks(np.arange(-0.5, len(mine), 1))
    ax.set_xticks(np.arange(-0.5, len(mine), 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    for (j, i), label in np.ndenumerate(temp_mine):
        ax.text(i, j, int(label))

    plt.show()
