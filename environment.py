import numpy as np

#This is what each cell holds
class Cell():
     def __init__(self, value, hidden, flag, hidden_neighbors_list,hidden_neighbors_count,reveal_safe_neighbors):
        #Clue
        self.value = value
        # If cell is hidden or revealed
        self.hidden = hidden
        # Mine flag
        self.flag = flag
        # List of coordinates of each hidden neighbor
        self.hidden_neighbors_list = hidden_neighbors_list
        # Number of hidden neighbors
        self.hidden_neighbors_count = hidden_neighbors_count
        # Number of safe neighbors uncovered
        self.reveal_safe_neighbors = reveal_safe_neighbors


def create_mine_sweeper(dim, num_mines):
    size = np.product(dim)
    mine_field = np.zeros(size, dtype=object)
    index = np.random.choice(np.arange(size), num_mines)
    while len(np.unique(index)) != num_mines:
        index = np.random.choice(np.arange(size), num_mines)
    mine_field[index] = -1
    mine_field = mine_field.reshape(dim)
    mine_field = input_count(mine_field)

    #Change the entire matrix from int to type Cell
    for x in range(len(mine_field)):
        for y in range(len(mine_field[x])):
            temp = mine_field[x][y]
           # temp1 = safe_neighbor_check((x,y), mine_field,1)[0]
           # temp2 = safe_neighbor_check((x,y), mine_field,1)[1]
           # temp3 = safe_neighbor_check((x,y), mine_field,0)[1]
            # This is a place holder for the attributes
            mine_field[x][y] = Cell(temp, True, False, [], 0, 0)

    # Fill in the correct attributes for each cell
    for x in range(len(mine_field)):
        for y in range(len(mine_field[x])):
            temp = mine_field[x][y].value
            temp1 = hidden_neighbor_check((x,y), mine_field)[0]
            temp2 = hidden_neighbor_check((x,y), mine_field,)[1]
            mine_field[x][y] = Cell(temp, True, False, temp1, temp2, 0)
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
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1] != -1:
        mine_field[x - 1, y - 1] += 1

    # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1] != -1:
        mine_field[x - 1, y + 1] += 1

    # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1] != -1:
        mine_field[x + 1, y - 1] += 1

    # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1] != -1:
        mine_field[x + 1, y + 1] += 1

def hidden_neighbor_check(pair, mine_field):
    (x,y) = pair
    count = 0
    list = []
    # Checks Top Neighboring cell and checks if neighbor is hidden
    if x - 1 >= 0 and mine_field[x - 1, y].hidden == True:
        count += 1
        list.append((x - 1,y))

        # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1].hidden == True:
        count += 1
        list.append((x,y - 1))

        # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1].hidden == True:
       count += 1
       list.append((x,y + 1))

    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y].hidden == True:
        count += 1
        list.append((x + 1,y))

        # Check to Upper Left Cell
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1].hidden == True:
        count += 1
        list.append((x-1,y-1))

        # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1].hidden == True:
        count += 1
        list.append((x-1,y+1))

        # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1].hidden == True:
        count += 1
        list.append((x+1,y-1))

        # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1].hidden == True :
        count += 1
        list.append((x+1,y+1))
    return list, count
