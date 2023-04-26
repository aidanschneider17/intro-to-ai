import numpy as np

def open_maze():
    """
    Maze where all tiles are walkable and the start and
    end positions are on opposite ends
    """
    maze = np.ones((5, 5))

    start = (4, 0)
    end = (0,4)

    return start,end,maze


def deceptive_maze3():
    """
    Maze where all tiles are walkable except a 1x3 vertical.
    Start and end positions are on the left and right side of the wall.
    """
    maze = np.ones((4, 4))
    maze[0:3,2] = 0
    start = (1,0)
    end = (1,3)
    return start,end,maze


def deceptive_maze4():
    """
    Maze where all tiles are walkable except a 1x4 L shape wall.
    Start and end positions are on the left and right side of the wall.
    """
    maze = np.ones((4, 4))
    maze[0:3, 2] = 0
    maze[2,1] = 0
    start = (1, 0)
    end = (1, 3)
    return start, end, maze





#
# def deceptive_maze1():
#     """
#     Maze where all tiles are walkable except a 1x3 horizontal
#     wall in the middle. Start and end positions are in the center
#     of the maze below and above the wall.
#     """
#     maze = np.ones((5, 5))
#     maze[2,1:4] = 0
#     start = (4,2)
#     end = (0,2)
#     return start,end,maze
#
#
# def deceptive_maze2():
#     """
#     Deceptive maze from the InformedSearch assignment.
#     """
#     maze = np.ones((5, 5))
#     maze[1,1:] = 0
#     maze[3,1:4] = 0
#
#     start = (4,2)
#     end = (0,4)
#     return start,end,maze