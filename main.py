import Agent
import Enviroment
import search

if __name__ == '__main__':
    environment = Enviroment.Environment("map1.txt")
    print("initial")
    environment.showEnvironment()
    print("\n")
    agent_on_grid = Agent.GrassCuttingAgent(environment.grid2D)
    print("Depth first search")
    search_DFS = Agent.depth_first_search(agent_on_grid)
    print("BFS")
    environment.showEnvironment()
    search_BFS = search.breadth_search(agent_on_grid)
