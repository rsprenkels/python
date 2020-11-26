from collections import defaultdict
from typing import DefaultDict, Tuple, List, Dict, Sequence

nodes = set()
graph: DefaultDict[str, List[Tuple[str, int]]] = defaultdict(list)

with open('2015_09_input.txt' , 'r') as f:
    for line in f.readlines():
        route, distance = line.rstrip().split(' = ')
        src, dest = route.split(' to ')
        nodes |= {src, dest}
        graph[src].append((dest, int(distance)))
        graph[dest].append((src, int(distance)))

    print(nodes)
    print(graph)
    shortest = 999999999999999999999999999999999999999999
    for start in nodes:
        seen: Dict[str, int] = {start: 0}
        Q: List[Tuple[str, int]] = [(start, 0)]
        while Q:
            node, dist_so_far = Q.pop(0)
            for reachable, dist in graph[node]:
                if reachable not in seen:
                    seen[reachable] = dist_so_far + dist
                    Q.append((reachable, dist_so_far + dist))
        if len(seen) == len(nodes):
            d = max([seen[node] for node in seen])
            shortest = min(shortest, d)
    print(f'part 1: {shortest}')
    # 128 is too high
    # 62 is wrong



def buttonbashing(buttons: Sequence[int], target: int) -> Tuple[int, int]:
    seen: Dict[int, int] = {0: 0}
    Q = [(0, 0)]
    solution = None
    while Q:
        value, clicks = Q.pop(0)
        for reachable in [value + button for button in buttons]:
            reachable = min(max(reachable, 0), 3600)
            if reachable not in seen or seen[reachable] > clicks + 1:
                seen[reachable] = clicks + 1
                Q.append((reachable, clicks + 1))
    cook_time = min(k for k in seen.keys() if k >= target)
    return (seen[cook_time], cook_time - target)
