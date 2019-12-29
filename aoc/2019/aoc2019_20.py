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


def readmaze(lines: str) -> Dict:
    maze = defaultdict(str)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            maze[P(x,y)] = c
    labels = defaultdict(list)
    xmin, xmax, ymin, ymax = get_maze_dimensions(maze)
    find_labels_x(labels, maze, at_row=0, offset=2)
    find_labels_x(labels, maze, at_row=ymax-1, offset=-1)
    find_labels_x(labels, maze, at_row=10, offset=2)
    find_labels_x(labels, maze, at_row=7, offset=-1)
    print(labels)

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
    m = readmaze(lines)
    print(m)