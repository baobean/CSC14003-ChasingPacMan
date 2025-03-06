from collections import deque
import heapq
import tracemalloc
import time

def bfs_algorithm(map_state, positions):
    """return the next appropriate move"""

    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    queue = deque([start])
    visited = set([start])
    parent = {}

    # Set things up for tracking
    expanded_nodes = 0  
    tracemalloc.start()  
    start_time = time.time() 

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

            return path[::-1][0] if path else start, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)

            if next_pos not in visited and map_state[next_pos[0]][next_pos[1]] == 0 and next_pos not in other_ghosts:
                queue.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    execution_time = time.time() - start_time
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()  # Stop memory tracking

    return (-1, -1), expanded_nodes, memory_usage  # No path found

#DFS algorithm, return a path from current position to goal and expanded_nodes

def dfs_algorithm(map_state, positions):
    return (-1, -1)

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
