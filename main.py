import advanced_strategy
import environment
import show_mine
import agent
import graph
import numpy as np

if __name__ == '__main__':
    mine_field = environment.create_mine_sweeper((3, 3), 4)
    advanced_strategy.play(mine_field, 4)
    show_mine.show(mine_field)
    print("Done")
    graph.graph((15, 15))
