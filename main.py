import environment
import show_mine
import agent
if __name__ == '__main__':
    mine_field = environment.create_mine_sweeper((3, 3), 1)
    agent.play(mine_field)
    show_mine.show(mine_field)

