import copy
from collections import deque

from Agent import Agent, Actions


class Node:

    def __init__(self, states, parent=None, actions=None, cost=0):
        self.states = states
        self.parent = parent
        self.actions = actions
        self.cost = cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.states)

    def __lt__(self, node):
        return self.states < node.states

    def expand(self, agent):
        return [self.child_node(agent, action)
                for action in agent.actions(self.states)]

    def child_node(self, agent, action):
        next_state = agent.position_result(self.states, action)
        next_node = Node(next_state, self, action, agent.cost(self.cost, self.states, action, next_state))
        return next_node

    def solution(self):
        return [node.actions for node in self.agent_path()[1:]]

    def agent_path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.states == other.states

    def __hash__(self):
        return hash(self.states)


def is_initial(state):
    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if state[i][j] == 'C':
                return False
    return True


'''
the search used in this project is depth first search to cut all the grass in the environment
'''


def depth_first_search(agent):
    frontier = [Node(agent.initial)]
    while frontier:
        node = frontier.pop()
        if agent.reward_movement(node.states):
            for i in range(len(node.agent_path())):
                showEnvironment(node.agent_path()[i].states)
                print("\n")
            return node
        frontier.extend(node.expand(agent))
    return None


'''
create the state of the agent movement and if it can search through the environment
'''


class GrassCuttingAgent(Agent):

    def cost(self, c, state1, action, state2):
        return 1

    def __init__(self, initial):
        super().__init__(initial=initial)
        self.initial = initial

    def actions(self, states):
        actions = []
        env = copy.deepcopy(states)
        currentState = [list(item) for item in env]
        if is_initial(states):
            actions.append(self.display_Grass(currentState))
        else:
            row = self.current_Position(states)[0]
            col = self.current_Position(states)[1]
            if row > 0 and currentState[row - 1][col] == 'G':
                actions.append(Actions.GONORTH)
            if row < len(states) - 1 and currentState[row + 1][col] == 'G':
                actions.append(Actions.GOSOUTH)
            if col < len(states[0]) and currentState[row][col + 1] == 'G':
                actions.append(Actions.GOEAST)
        return actions

    def position_result(self, state, action):
        env = copy.deepcopy(state)
        currentState = [list(item) for item in env]
        if len(self.current_Position(state)) == 0:
            currentState[action[0]][0] = 'X'
        else:
            x = self.current_Position(currentState)[0]
            y = self.current_Position(currentState)[1]
            currentState[x][y] = 'C'
            if action == Actions.GONORTH:
                currentState[x - 1][y] = 'X'
            elif action == Actions.GOSOUTH:
                currentState[x + 1][y] = 'X'
            else:
                currentState[x][y + 1] = 'X'

        return tuple(map(tuple, currentState))

    def number_states(self, state):
        return 1

    def display_Grass(self, state):
        next_grass = []
        for i in range(len(state)):
            if state[i][0] == 'G':
                next_grass.append(i)
        return next_grass

    def current_Position(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 'X':
                    return [i, j]
        return []

    def reward_movement(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 'G':
                    if i > 0 and state[i - 1][j] == '0':
                        if i < len(state) - 1 and state[i + 1][j] == '0':
                            if j < len(state[0]) - 1 and state[i][j + 1] == '0':
                                if j > 0 and state[i][j - 1] == '0':
                                    continue
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
        return True


def showEnvironment(state):
    for rows in range(len(state)):
        for cols in range(len(state)):
            print(state[rows][cols], end=' ')
        print("  ")


def breadth_search(agent):
    frontier = deque([Node(agent.initial)])

    while frontier:
        node = frontier.popleft()
        if agent.reward_movement(node.states):
            return node
        frontier.extend(node.expand(agent))
    return None

