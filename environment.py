import numpy as np


def create_mine_sweeper(dim, num_mines):
    size = np.product(dim)
    mine_field = np.zeros(size, dtype=np.int)
    index = np.random.choice(np.arange(size), num_mines)
    while len(np.unique(index)) != num_mines:
        index = np.random.choice(np.arange(size), num_mines)
    mine_field[index] = -1
    mine_field = mine_field.reshape(dim)
    mine_field = input_count(mine_field)
    return mine_field


def input_count(mine_field):
    for i in range(len(mine_field)):
        for j in range(len(mine_field[i])):
            if mine_field[i, j] == -1:
                increment_neighbors((i, j), mine_field)
                # print(mine_field)

    return mine_field


def increment_neighbors(pair, mine_field):
    (x, y) = pair

    # Checks Top Neighboring cell
    if x - 1 >= 0 and mine_field[x - 1, y] != -1:
        mine_field[x - 1, y] += 1

    # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1] != -1:
        mine_field[x, y - 1] += 1

    # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1] != -1:
        mine_field[x, y + 1] += 1

    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y] != -1:
        mine_field[x + 1, y] += 1

    # Check to Upper Left Cell
    if x - 1 > 0 and y - 1 > 0 and mine_field[x - 1, y - 1] != -1:
        mine_field[x - 1, y - 1] += 1

    # Check the Upper Right Cell
    if x - 1 > 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1] != -1:
        mine_field[x - 1, y + 1] += 1

    # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 > 0 and mine_field[x + 1, y - 1] != -1:
        mine_field[x + 1, y - 1] += 1

    # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1] != -1:
        mine_field[x + 1, y + 1] += 1
