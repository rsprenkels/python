from collections import defaultdict
from typing import Dict
from aoc import P


def get_maze_dimensions(maze):
    xmin = min(p.x for p in maze)
    xmax = max(p.x for p in maze)
    ymin = min(p.y for p in maze)
    ymax = max(p.y for p in maze)
    return xmin, xmax, ymin, ymax


def find_labels_x(labels, maze, at_row, offset):
    xmin, xmax, ymin, ymax = get_maze_dimensions(maze)
    for x in range(xmin, xmax + 1):
        if maze[P(x, at_row)].isupper():
            labels[maze[P(x, at_row)] + maze[P(x, at_row + 1)]].append(P(x, at_row + offset))


def find_labels_y(labels, maze, at_col, offset):
    xmin, xmax, ymin, ymax = get_maze_dimensions(maze)
    for y in range(ymin, ymax + 1):
        if maze[P(at_col, y)].isupper():
            labels[maze[P(at_col, y)] + maze[P(at_col + 1, y)]].append(P(at_col + offset, y))


def readmaze(lines: str) -> Dict:
    maze = defaultdict(str)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            maze[P(x,y)] = c
    labels = defaultdict(list)
    xmin, xmax, ymin, ymax = get_maze_dimensions(maze)
    for y, x in ((y, x) for y in range(2, ymax // 2) for x in range (2, xmax - 2)):
        if maze[P(x, y)] not in '/#.':
            donut_width = y - 2
            break
    find_labels_x(labels, maze, at_row=0, offset=2)
    find_labels_x(labels, maze, at_row=ymax-1, offset=-1)
    find_labels_x(labels, maze, at_row=donut_width + 2, offset=-1)
    find_labels_x(labels, maze, at_row=ymax - donut_width - 3, offset=2)
    find_labels_y(labels, maze, at_col=0, offset=2)
    find_labels_y(labels, maze, at_col=xmax-1, offset=-1)
    find_labels_y(labels, maze, at_col=donut_width + 2, offset=-1)
    find_labels_y(labels, maze, at_col=xmax - donut_width - 3, offset=2)
    return maze, labels

def test_readmaze_1():
    lines = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
""".split('\n')[1:-1]
    maze, labels = readmaze(lines)
