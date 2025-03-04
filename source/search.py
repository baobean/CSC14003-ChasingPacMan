from collections import deque
import heapq

def bfs_algorithm(map_state, positions):
    return (-1, -1)  # No path found

#DFS algorithm, return a path from current position to goal
def dfs(map_state, current_position, goal, path, visited, expanded_node):
    #Check if the given position is valid within the map_state
    #mapstate[x][y] = -1 means there's an obstacle there
    def is_valid(map_state, position):
        x, y = position[0], position[1]
        return 0 <= x < len(map_state) and 0 <= y < len(map_state[0]) and map_state[x][y] != -1
    if current_position == goal:
        return path
    
    visited.add(current_position)
    expanded_node += 1
    #right, left, up, down
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    
    #go right, left, up, down to find a goal
    for direction in directions:
        next_position = (current_position[0] + direction[0], current_position[1] + direction[1])
        if is_valid(map_state, next_position) and next_position not in visited: #if this is valid position, keep going
            path = dfs(map_state, next_position, goal, path + [next_position], visited) 
            if path: # if the path is found, return path
                return path
    visited.remove(current_position)

    #return empty array if can't find a path
    return []

def dfs_algorithm(map_state, positions):
    path = []
    visited = set()
    
    expanded_nodes = 0  # Count expanded nodes
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Track execution time
    
    path = dfs(map_state, positions["pink ghost"], positions["pacman"], [], visited, expanded_node)
    
    # if the path is not empty, return the next position to move
    if path:
        execution_time = time.time() - start_time  # Compute elapsed time
        memory_usage = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return path[0], execution_time, expanded_nodes, memory_usage
    execution_time = time.time() - start_time  # Compute elapsed time
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return (-1, -1), execution_time, expanded_nodes, memory_usage # No path found

import heapq
import time
import tracemalloc  # Memory tracking

def ucs_algorithm(map_state, positions):
    """Uniform-Cost Search for a specific ghost, avoiding other ghosts"""

    start = positions["ghost"]  # The ghost that is currently moving
    goal = positions["pacman"]  # Pac-Man's position
    other_ghosts = set(positions["ghosts"])  # Other ghosts' positions

    pq = [(0, start)]  # Priority queue (cost, position)
    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    expanded_nodes = 0  # Count expanded nodes
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Track execution time

    while pq:
        cost, current = heapq.heappop(pq)
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]

            execution_time = time.time() - start_time  # Compute elapsed time
            memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
            tracemalloc.stop()

            return path[::-1][0] if path else start, execution_time, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # Right → Up → Left → Down
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + 1  # Each move has cost = 1

            if next_pos not in visited and map_state[next_pos[1]][next_pos[0]] == 0 and next_pos not in other_ghosts:
                heapq.heappush(pq, (new_cost, next_pos))
                visited.add(next_pos)
                parent[next_pos] = current
                cost_so_far[next_pos] = new_cost

    execution_time = time.time() - start_time  # Compute elapsed time
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return (-1, -1), execution_time, expanded_nodes, memory_usage  # No path found



def astar_algorithm(map_state, positions):
    return (-1, -1)
