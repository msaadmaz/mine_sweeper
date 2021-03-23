import environment
import agent
import numpy as np
import matplotlib.pyplot as plt

def graph(dim):
    """
    Method to Plot,  for  Basic Agent and Improved Agent,
    a  graph  of  ‘Mining Density’  vs  ‘Average Final Score
    :param dim
    :return: v
    """
    x = 0.1
    count = 0
    score = 0
    score2 = 0
    y1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    y2 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    x1 = np.array([])
    x2 = np.array([])
    while x < 1:
        for i in range(10):
            mines = dim[0] * dim[1]
            mine_field = environment.create_mine_sweeper(dim, mines)
            score += agent.play(mine_field)
            # score2 = advanced_strategy.advance_strategy(mine_field)
        score = score/10
       # score2 = score2/10
        #x2 = np.append(x2, [score2])
        x1 = np.append(x1, [1])
        x+=0.1
    # Generate Graph of strat 1,2, and 3
    plt.plot(x1, y1, label="Basic Agent")
   # plt.plot(x2, y2, label="Improved Agent")
    plt.ylabel("Mine Density")
    plt.xlabel("Avg Final Score")
    plt.legend()
    plt.title("Basic Agent vs Important Agent")
    plt.show()