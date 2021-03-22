import environment
import show_mine
import agent
if __name__ == '__main__':
    mine_field = environment.create_mine_sweeper((5, 5), 5)
    agent.play(mine_field)
    show_mine.show(mine_field)

