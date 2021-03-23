import environment
import numpy as np
import random

revealed_mine = 0

mine_flagged = 0
safe_set = set()

# This will make a fringe of hidden neigbors
def make_list(mine_field):
    total_hidden_cells = []
    for x in range(len(mine_field)):
        for y in range(len(mine_field[x])):
            total_hidden_cells.append((x, y))
    return total_hidden_cells


# Method p@r@meters: environment, cell, i and j indices, fringe
def play(mine_field):
    # Make the fringe
    fringe = make_list(mine_field)

    # debugger coutner
    counter = 1
    while len(fringe):
        index = random.randint(0, len(fringe) - 1)
        a = fringe[index]
        print(f'This is iteration {counter} and the index is {a}')
        query(mine_field, mine_field[a[0], a[1]], a[0], a[1], fringe)
        counter += 1
        global safe_set
        while safe_set:
            (s,t) = safe_set.pop()
         #   print((s,t))
            query(mine_field, mine_field[s, t], s ,t, fringe)



    global revealed_mine
    global mine_flagged
    total_mines = revealed_mine+mine_flagged
    if(total_mines!=0):
        final_score = mine_flagged/total_mines
    else:
        final_score = 0
    print(f'this is final score: {final_score}')
    return final_score


def query(mine_field, target, i, j, fringe):
    # Selected cell
    selected = target

    # Uncover the cell
    selected.hidden = False

    # counter for amount of times bomb is selected
    counter = 0

    # If cell is a bomb
    if selected.value == 1:
        counter += 1
        print(f"Bomb has been selected {counter} times")
        global revealed_mine
        revealed_mine += 1  # Mine went off and is now revealed mine
        increment_Safe_decrement_hidden((i, j), mine_field, 1)
        fringe.remove((i, j))
        return fringe

    # Since cell is revealed and safe, update safe_neighbors attribute for its neighbors
    else:
        increment_Safe_decrement_hidden((i, j), mine_field, 0)
        increment_Safe_decrement_hidden((i, j), mine_field, 1)

    # Remove from Fringe
    fringe.remove((i, j))

    #  If the total number of mines (the clue) minus the number of revealed mines is the number of hidden neighbors,
    if (selected.clue - revealed_mine) == selected.hidden_neighbors_count:
        print("Mines are being flagged")
        # Every Hidden Neighbor is a Mine
        # counter for mines being flagged
        counter2 = 0
        for (x, y) in selected.hidden_neighbors_list:
            # Mark each neighbor w/ flag
            mine_field[x, y].flag = True
            counter2 += 1
            print(f'{counter2} mines have been flagged')
            global mine_flagged
            mine_flagged += 1
            increment_Safe_decrement_hidden((x, y), mine_field, 1)
            fringe.remove((x, y))

    # If the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors is the number of
    # hidden neighbors
    # If cell is any of 4 corners, max neighbors is 3, not 8
    n = neighbor_count((i,j), mine_field)
    total_safe = n - selected.clue
    hidden_safe_neighbors = total_safe - selected.reveal_safe_neighbors
    if hidden_safe_neighbors == selected.hidden_neighbors_count:
        print("Going through safe neighbors")

        # counter for safe neighbors
        #counter3 = 0
        # Every Hidden Neighbor is Safe
        for (x,y) in selected.hidden_neighbors_list:
            print(len(selected.hidden_neighbors_list))
            # # This means that the cell has already been uncovered and queried
            # if fringe.count((x, y)) == 0:
            #     continue
            # Query each safe cell and recursively call check
            print (f'This is the safe cell being checked: {(x, y)}')
            global safe_set
            safe_set.add((x,y))
           # print("Added")

        # Since each neighbor was safe and queried, empty the list
        #selected.hidden_neighbors_list.clear()
        # Reset hidden neigbors
        #selected.hidden_neighbors_count = 0
    return fringe


def increment_Safe_decrement_hidden(pair, mine_field, mode):
    (x, y) = pair
    # Checks Top Neighboring cell
    if x - 1 >= 0 and mine_field[x - 1, y]:
        if (mode == 0):
            mine_field[x - 1, y].reveal_safe_neighbors += 1
        else:
            mine_field[x - 1, y].hidden_neighbors_count -= 1
            mine_field[x - 1, y].hidden_neighbors_list.remove((x, y))

    # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1]:
        if (mode == 0):
            mine_field[x, y - 1].reveal_safe_neighbors += 1
        else:
            mine_field[x, y - 1].hidden_neighbors_count -= 1
            mine_field[x, y - 1].hidden_neighbors_list.remove((x, y))
    # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1]:
        if (mode == 0):
            mine_field[x, y + 1].reveal_safe_neighbors += 1
        else:
            mine_field[x, y + 1].hidden_neighbors_count -= 1
            mine_field[x, y + 1].hidden_neighbors_list.remove((x, y))
    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y]:
        if (mode == 0):
            mine_field[x + 1, y].reveal_safe_neighbors += 1
        else:
            mine_field[x + 1, y].hidden_neighbors_count -= 1
            mine_field[x + 1, y].hidden_neighbors_list.remove((x, y))

    # Check to Upper Left Cell
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1]:
        if (mode == 0):
            mine_field[x - 1, y - 1].reveal_safe_neighbors += 1
        else:
            mine_field[x - 1, y - 1].hidden_neighbors_count -= 1
            mine_field[x - 1, y - 1].hidden_neighbors_list.remove((x, y))
    # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1]:
        if (mode == 0):
            mine_field[x - 1, y + 1].reveal_safe_neighbors += 1
        else:
            mine_field[x - 1, y + 1].hidden_neighbors_count -= 1
            mine_field[x - 1, y + 1].hidden_neighbors_list.remove((x, y))
    # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1]:
        if (mode == 0):
            mine_field[x + 1, y - 1].reveal_safe_neighbors += 1
        else:
            mine_field[x + 1, y - 1].hidden_neighbors_count -= 1
            mine_field[x + 1, y - 1].hidden_neighbors_list.remove((x, y))
    # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1]:
        if (mode == 0):
            mine_field[x + 1, y + 1].reveal_safe_neighbors += 1
        else:
            mine_field[x + 1, y + 1].hidden_neighbors_count -= 1
            mine_field[x + 1, y + 1].hidden_neighbors_list.remove((x, y))
def neighbor_count(pair, mine_field):
    (x, y) = pair
    count = 0
    if x - 1 >= 0 and mine_field[x - 1, y]:
        count+=1
    # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1]:
        count +=1
    # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1]:
        count +=1
    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y]:
        count +=1
    # Check to Upper Left Cell
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1]:
        count +=1
    # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1]:
        count +=1
    # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1]:
        count +=1
    # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1]:
        count +=1
    return count

#def check_safe_neighbors(mine_field, target, x, y, fringe):