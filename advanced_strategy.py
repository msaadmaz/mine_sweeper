from collections import namedtuple

from agent import increment_Safe_decrement_hidden, neighbor_count


def populate_hidden_cells(mine_field):
    hidden_cells = set()
    for x in range(len(mine_field)):
        for y in range(len(mine_field[x])):
            hidden_cells.add((x, y))

    return hidden_cells


Equation = namedtuple('Equation', ['hidden_neighbors', 'clue_value'])
safe_set = set()


# Method p@r@meters: environment, cell, i and j indices, fringe
def play(mine_field, num_mines):
    # make sets to mark different forms of tracking for cells
    known_safe_cells = set()
    open_cells = set()
    flagged_mines = set()
    fringe = set()
    hit_mines = set()

    fringe = populate_hidden_cells(mine_field)

    # counter for iteration
    iteration = 1

    while fringe:
        if num_mines == 0:
            break
        (x, y) = (0, 0)
        if iteration == 1:
            (x, y) = fringe.pop()
        else:
            num_mines, fringe = implement_strategy(open_cells, mine_field, known_safe_cells, flagged_mines, hit_mines,
                                                   fringe, num_mines)
            if not fringe:
                break
            else:
                (x, y) = fringe.pop()
        query(mine_field, mine_field[x, y], x, y, fringe, num_mines, known_safe_cells, open_cells, flagged_mines,
              hit_mines)
        global safe_set
        while safe_set:
            (s, t) = safe_set.pop()
            query(mine_field, mine_field[s, t], s, t, fringe, num_mines, known_safe_cells, open_cells, flagged_mines,
                  hit_mines)
        iteration += 1

    total_mines = len(hit_mines) + len(flagged_mines)
    print(len(flagged_mines))
    if total_mines != 0:
        final_score = len(flagged_mines) / total_mines
    else:
        final_score = 0
    print(f'this is final score: {final_score}')


def query(mine_field, target, i, j, fringe, num_mines, known_safe_cells, open_cells, flagged_mines, hit_mines):
    # Selected cell
    selected = target

    # Uncover the cell
    selected.hidden = False

    # If cell is a bomb
    if selected.value == 1:
        hit_mines.add((i, j))
        open_cells.add((i, j))
        increment_Safe_decrement_hidden((i, j), mine_field, 1)
        # fringe.remove((i, j))
        num_mines -= 1
        return fringe

    # Since cell is revealed and safe, update safe_neighbors attribute for its neighbors
    else:
        increment_Safe_decrement_hidden((i, j), mine_field, 0)
        increment_Safe_decrement_hidden((i, j), mine_field, 1)
        known_safe_cells.add((i, j))
        open_cells.add((i, j))

    # Remove from Fringe
    # fringe.remove((i, j))

    #  If the total number of mines (the clue) minus the number of revealed mines is the number of hidden neighbors,
    if (selected.clue - (len(hit_mines) + len(flagged_mines))) == selected.hidden_neighbors_count:
        # Every Hidden Neighbor is a Mine
        for (x, y) in selected.hidden_neighbors_list:
            # Mark each neighbor w/ flag
            num_mines -= 1
            mine_field[x, y].flag = True
            flagged_mines.add((i, j))
            increment_Safe_decrement_hidden((x, y), mine_field, 1)
            fringe.remove((x, y))

    # If the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors is the number of
    # hidden neighbors
    # If cell is any of 4 corners, max neighbors is 3, not 8
    n = neighbor_count((i, j), mine_field)
    total_safe = n - selected.clue
    hidden_safe_neighbors = total_safe - selected.reveal_safe_neighbors
    if hidden_safe_neighbors == selected.hidden_neighbors_count:
        # Every Hidden Neighbor is Safe
        for (x, y) in selected.hidden_neighbors_list:
            global safe_set
            safe_set.add((x, y))
            known_safe_cells.add((x, y))
    return fringe


def implement_strategy(open_cells, mine_field, known_safe_cells, flagged_mines, hit_mines, fringe, num_mines):
    knowledge_base = update_knowledge_base(open_cells, flagged_mines, hit_mines, mine_field)

    for equation1 in knowledge_base.values():
        for equation2 in knowledge_base.values():
            # check if the 2 equations are the same
            if equation1 == equation2:
                continue

            if equation2.clue_value > equation1.clue_value:
                continue

            num1_hidden_neighbors = equation1.hidden_neighbors
            num2_hidden_neighbors = equation2.hidden_neighbors

            # every cell that is not the same between the 2 sets should be marked
            unique_n1 = num1_hidden_neighbors - num2_hidden_neighbors
            unique_n2 = num2_hidden_neighbors - num1_hidden_neighbors
            new_cluevalue = equation1.clue_value - equation2.clue_value

            if len(unique_n1) == new_cluevalue:
                for neighbor in unique_n1:
                    # if the cell is hidden then it is a mine
                    if neighbor in fringe:
                        flagged_mines.add(neighbor)
                        fringe.remove(neighbor)
                        mine_field[neighbor].flag = True

                        # add this to the identified mines list
                        num_mines -= 1

                for neighbor in unique_n2:
                    if neighbor not in open_cells and neighbor in fringe:
                        known_safe_cells.add(neighbor)

    return num_mines, fringe


def update_knowledge_base(open_cells, flagged_mines, hit_mines, mine_field):
    # the knowledge base is a dictonary of equations
    knowledge_base = {}

    for cell in open_cells:
        # the cell is a mine
        if cell in flagged_mines or cell in hit_mines:
            continue

        # update neighbors information
        identified_mine_neighbors = get_identified_mine_neighbors(cell, mine_field)
        mines_remaining = mine_field[cell].clue - identified_mine_neighbors

        knowledge_base[cell] = Equation(hidden_neighbor_check(cell, mine_field), mines_remaining)

    return knowledge_base

def hidden_neighbor_check(pair, mine_field):
    (x, y) = pair
    count = 0
    list = set()
    # Checks Top Neighboring cell and checks if neighbor is hidden
    if x - 1 >= 0 and mine_field[x - 1, y].hidden == True:
        list.add((x - 1, y))

        # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1].hidden == True:
        list.add((x, y - 1))

        # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1].hidden == True:
        list.add((x, y + 1))

    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y].hidden == True:
        list.add((x + 1, y))

        # Check to Upper Left Cell
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1].hidden == True:
        list.add((x - 1, y - 1))

        # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1].hidden == True:
        list.add((x - 1, y + 1))

        # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1].hidden == True:
        list.add((x + 1, y - 1))

        # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1].hidden == True:
        list.add((x + 1, y + 1))
    return list


def get_identified_mine_neighbors(cell, mine_field):
    (x, y) = cell
    identified_mine_count = 0
    # Checks Top Neighboring cell
    if x - 1 >= 0 and mine_field[x - 1, y].value == 1 and mine_field[x - 1, y].flag:
        identified_mine_count += 1

    # Checks Left Neighboring cell
    if y - 1 >= 0 and mine_field[x, y - 1].value == 1 and mine_field[x, y - 1].flag:
        identified_mine_count += 1

    # Checks Right Neighboring cell
    if y + 1 < len(mine_field) and mine_field[x, y + 1].value == 1 and mine_field[x, y + 1].flag:
        identified_mine_count += 1

    # Checks the Bottom Cell
    if x + 1 < len(mine_field) and mine_field[x + 1, y].value == 1 and mine_field[x + 1, y].flag:
        identified_mine_count += 1

    # Check to Upper Left Cell
    if x - 1 >= 0 and y - 1 >= 0 and mine_field[x - 1, y - 1].value == 1 and mine_field[x - 1, y - 1].flag:
        identified_mine_count += 1

    # Check the Upper Right Cell
    if x - 1 >= 0 and y + 1 < len(mine_field) and mine_field[x - 1, y + 1].value == 1 and mine_field[
        x - 1, y + 1].flag:
        identified_mine_count += 1

    # Check the Lower Left Cell
    if x + 1 < len(mine_field) and y - 1 >= 0 and mine_field[x + 1, y - 1].value == 1 and mine_field[
        x + 1, y - 1].flag:
        identified_mine_count += 1

    # Check the Lower Right Cell
    if x + 1 < len(mine_field) and y + 1 < len(mine_field) and mine_field[x + 1, y + 1].value == 1 and mine_field[
        x + 1, y + 1].flag:
        identified_mine_count += 1

    return identified_mine_count
