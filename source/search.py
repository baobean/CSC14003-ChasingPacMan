from collections import deque
import heapq
import tracemalloc
import time

def bfs_algorithm(map_state, positions):
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    queue = deque([start])
    visited = set([start])
    parent = {}

    expanded_nodes = 0  
    tracemalloc.start()  

    while queue:
        current = queue.popleft()
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]

            memory_usage = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            if path:
                next_move = path[::-1][0] 

                if next_move in other_ghosts and next_move != goal:
                    next_move = start 
            else: 
                next_move = start 

            return next_move, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)

            if map_state[next_pos[1]][next_pos[0]] == float('inf'): 
                continue

            if next_pos not in visited:
                queue.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()  
    return (-1, -1), expanded_nodes, memory_usage  


def dls(curr_pos, goal, depth, map_state, other_ghosts, visited, parent):
    if depth >= 0:
        if curr_pos == goal:
            return curr_pos
        visited.add(curr_pos)

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (curr_pos[0] + dx, curr_pos[1] + dy)
            
            if next_pos not in visited and map_state[next_pos[1]][next_pos[0]] != float('inf'):
                parent[next_pos] = curr_pos
                found = dls(next_pos, goal, depth - 1, map_state, other_ghosts, visited, parent)
                if found:
                    return found
        visited.remove(curr_pos)
    return None

def ids_algorithm(map_state, positions):
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    expanded_nodes = 0  
    tracemalloc.start()  

    depth = 0
    while True:
        visited = set()
        parent = {}
        result = dls(start, goal, depth, map_state, other_ghosts, visited, parent)
        expanded_nodes += len(visited)
        if result:
            path = []
            current_pos = result
            while current_pos != start:
                path.append(current_pos)
                current_pos = parent[current_pos]

            memory_usage = tracemalloc.get_traced_memory()[1] 
            tracemalloc.stop()
            if path:
                next_move = path[::-1][0] 

                if next_move in other_ghosts and next_move != goal:
                    next_move = start 
            else:
                next_move = start 

            return next_move, expanded_nodes, memory_usage
        depth += 1

        if depth > len(map_state) * len(map_state[0]):
            break

    memory_usage = tracemalloc.get_traced_memory()[1]  
    tracemalloc.stop()
    return (-1, -1), expanded_nodes, memory_usage

def ucs_algorithm(map_state, positions):

    start = positions["ghost"]  
    goal = positions["pacman"] 
    other_ghosts = set(positions["ghosts"])  

    cell_value = map_state[goal[1]][goal[0]]  
    map_state[goal[1]][goal[0]] = -10 

    pq = [(0, start)]  
    visited = set() 
    parent = {start: None}
    cost_so_far = {start: 0}

    expanded_nodes = 0  
    tracemalloc.start()  

    while pq:
        cost, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]

            memory_usage = tracemalloc.get_traced_memory()[1]  
            tracemalloc.stop()

            if path:
                next_move = path[::-1][0] 

                if next_move in other_ghosts and next_move != goal:
                    next_move = start 
            else: 
                next_move = start 

            map_state[goal[1]][goal[0]] = cell_value  
            return next_move, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + map_state[next_pos[1]][next_pos[0]]

            if map_state[next_pos[1]][next_pos[0]] == float('inf'): 
                continue

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                heapq.heappush(pq, (new_cost, next_pos))
                parent[next_pos] = current
                cost_so_far[next_pos] = new_cost

    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    map_state[goal[1]][goal[0]] = cell_value 
    return (-1, -1), expanded_nodes, memory_usage  
    
def astar_algorithm(map_state, positions):
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    pq = [(0, start)]
    parent = {}
    cost_so_far = {start: 0}

    expanded_nodes = 0
    tracemalloc.start()

    while pq:
        cost, current = heapq.heappop(pq)
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]

            memory_usage = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            if path:
                next_move = path[::-1][0] 

                if next_move in other_ghosts and next_move != goal:
                    next_move = start 
            else: 
                next_move = start 

            return next_move, expanded_nodes, memory_usage
        
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + 1

            if map_state[next_pos[1]][next_pos[0]] == float('inf'): 
                continue

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + abs(goal[0] - next_pos[0]) + abs(goal[1] - next_pos[1])
                heapq.heappush(pq, (priority, next_pos))
                parent[next_pos] = current

    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return (-1, -1), expanded_nodes, memory_usage
