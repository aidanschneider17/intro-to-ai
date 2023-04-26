import collections

from Problem import *
from queue import PriorityQueue


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


def a_star(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
     well as search operators (metohds). Performs A*
     and returns the path found. Returns and empty list is no path is found.
     """

    node = Node(problem.initial)

    if problem.is_goal(node.state):
        return get_path(node)

    entry = 0
    frontier = PriorityQueue()
    cost = problem.estimated_cost(node.state) + node.path_cost
    frontier.put((cost, entry, node))
    entry += 1

    reached = {problem.hashable_state(node.state): node}

    while frontier.qsize() != 0:
        node = frontier.get()[2]

        if problem.is_goal(node.state):
            return get_path(node)

        for child in problem.expand(node):
            s = child.state

            if problem.hashable_state(s) not in reached:
                reached[problem.hashable_state(s)] = child
                cost = problem.estimated_cost(s) + child.path_cost
                frontier.put((cost, entry, child))
                entry += 1

    return []


def greedy(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
     well as search operators (metohds). Performs a Greedy Search
     and returns the path found. Returns and empty list is no path is found.
     """

    node = Node(problem.initial)

    if problem.is_goal(node.state):
        return get_path(node)

    entry = 0
    frontier = PriorityQueue()
    cost = problem.estimated_cost(node.state)
    frontier.put((cost, entry, node))
    entry += 1

    reached = {problem.hashable_state(problem.initial): node}

    while frontier.qsize() != 0:
        node = frontier.get()[2]

        if problem.is_goal(node.state):
            return get_path(node)

        for child in problem.expand(node):
            s = child.state

            if problem.hashable_state(s) not in reached:
                reached[problem.hashable_state(s)] = child
                cost = problem.estimated_cost(s)
                frontier.put((cost, entry, child))
                entry += 1

    return []
