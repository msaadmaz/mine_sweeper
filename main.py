import advanced_strategy
import environment
import show_mine
import agent
import numpy as np
if __name__ == '__main__':
    mine_field = environment.create_mine_sweeper((3, 3), 4)
    # mine_field = np.array([[0,2,-1],[2,4,-1],[-1,-1,2]], dtype = object)
    # print(mine_field)
    # for x in range(len(mine_field)):
    #     for y in range(len(mine_field[x])):
    #         temp = mine_field[x][y]
    #         if temp == -1:
    #             mine_field[x][y] = environment.Cell(1, True, False, [], 0, 0, 0)
    #         else:
    #             mine_field[x][y] = environment.Cell(0, True, False, [], 0, 0, temp)
    #
    # # Fill in the correct attributes for each cell
    # for x in range(len(mine_field)):
    #     for y in range(len(mine_field[x])):
    #         temp1 = environment.hidden_neighbor_check((x, y), mine_field)[0]
    #         temp2 = environment.hidden_neighbor_check((x, y), mine_field)[1]
    #         mine_field[x][y].hidden_neighbors_list = temp1
    #         mine_field[x][y].hidden_neighbors_count = temp2
    # agent.play(mine_field)
    advanced_strategy.play(mine_field, 4)
    show_mine.show(mine_field)
    print("Done")

