import environment
import agent
if __name__ == '__main__':
    mine_field = environment.create_mine_sweeper((3, 3), 1)
    agent.play(mine_field)

