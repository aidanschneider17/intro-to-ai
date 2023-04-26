from Problem import *
from collections import deque


def get_path(node: Node)->List[str]:
    """
    Takes in a Node object and returns
    a reversed list of actions from that node to its root.
    """
    root = node
    p = []
    while root is not None:
        p.append(root.action)
        root = root.parent
    p.reverse()
    return p


def breadth_first_search(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
     well as search operators (metohds). Performs a Breadth First Search
     and returns the path found using the get_path method. For example,
     return get_path(node), where node is the node with a state that
      matches the goal. Returns and empty list if no path is found.
     """
    node = Node(problem.initial)

    if problem.is_goal(node.state):
        return get_path(node)

    frontier = deque([node])
    reached = {problem.hashable_state(problem.initial): problem.initial}

    while len(frontier) != 0:
        node = frontier.popleft()

        for child in problem.expand(node):
            s = child.state

            if problem.is_goal(s):
                return get_path(child)

            if problem.hashable_state(s) not in reached:
               reached[problem.hashable_state(s)] = s
               frontier.append(child) 

    return []


def depth_first_search(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
     well as search operators (metohds). Performs a Depth First Search
     and returns the path found using the get_path method. For example,
     return get_path(node), where node is the node with a state that
      matches the goal. Returns and empty list if no path is found.
     """
    node = Node(problem.initial)

    if problem.is_goal(node.state):
        return get_path(node)

    frontier = deque([node])
    reached = {problem.hashable_state(problem.initial): problem.initial}

    while len(frontier) != 0:
        node = frontier.pop()

        for child in problem.expand(node):
            s = child.state

            if problem.is_goal(s):
                return get_path(child)

            if problem.hashable_state(s) not in reached:
               reached[problem.hashable_state(s)] = s
               frontier.append(child) 

    return []