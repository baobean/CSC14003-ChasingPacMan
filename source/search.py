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

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)

            if 0 <= next_pos[0] < len(map_state[0]) and 0 <= next_pos[1] < len(map_state) and next_pos not in visited and map_state[next_pos[1]][next_pos[0]] != float('inf') and next_pos not in other_ghosts:
                queue.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()  # Stop memory tracking

    return (-1, -1), expanded_nodes, memory_usage  # No path found

#DFS algorithm, return a path from current position to goal and expanded_nodes

def dfs_algorithm(map_state, positions):
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])


    expanded_nodes = 0  # Count expanded nodes
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Track execution time

    stack = []
    visited = set(start)
    parent = {}
    stack.append(start)

    while stack:
        expanded_nodes += 1
        current_pos = stack.pop(0)
        if current_pos == goal:
            path = []
            while current_pos != start:
                path.append(current_pos)
                current_pos = parent[current_pos]

            execution_time = time.time() - start_time  # Compute elapsed time
            memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
            tracemalloc.stop()
            return path[::-1][0] if path else start, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            if next_pos not in visited and next_pos not in other_ghosts and map_state[next_pos[0]][next_pos[1]] == 0:
                parent[next_pos] = current_pos
                visited.add(next_pos)
                stack.append(next_pos)
    execution_time = time.time() - start_time  # Compute elapsed time
    memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    return (-1, -1), expanded_nodes, memory_usage



def dls(curr_pos, goal, depth, map_state, other_ghosts, visited, parent):
    # Depth-Limited Search (DLS) function
    if depth >= 0:
        if curr_pos == goal:
            # If the current position is the goal, return the current position
            return curr_pos
        visited.add(curr_pos)
        # Explore the four possible directions (up, left, down, right)
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (curr_pos[0] + dx, curr_pos[1] + dy)
            # Check if the next position is valid and not visited
            if next_pos not in visited and next_pos not in other_ghosts and map_state[next_pos[0]][next_pos[1]] == 0:
                parent[next_pos] = curr_pos
                # Recursive call to DLS with decremented depth
                found = dls(next_pos, goal, depth - 1, map_state, other_ghosts, visited, parent)
                if found:
                    return found
        visited.remove(curr_pos)
    return None

def ids_algorithm(map_state, positions):
    # Iterative Deepening Search (IDS) algorithm
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    expanded_nodes = 0  # Count expanded nodes
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Track execution time

    depth = 0
    while True:
        visited = set()
        parent = {}
        # Perform Depth-Limited Search (DLS) up to the current depth
        result = dls(start, goal, depth, map_state, other_ghosts, visited, parent)
        expanded_nodes += len(visited)
        if result:
            # If goal is found, reconstruct the path
            path = []
            current_pos = result
            while current_pos != start:
                path.append(current_pos)
                current_pos = parent[current_pos]

            execution_time = time.time() - start_time  # Compute elapsed time
            memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
            tracemalloc.stop()
            return path[::-1][0] if path else start, expanded_nodes, memory_usage
        depth += 1

        # If depth exceeds a reasonable limit, break to prevent infinite loop
        if depth > len(map_state) * len(map_state[0]):
            break

    execution_time = time.time() - start_time  # Compute elapsed time
    memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    return (-1, -1), expanded_nodes, memory_usage

def ucs_algorithm(map_state, positions):
    """Uniform-Cost Search for a specific ghost, avoiding other ghosts"""

    start = positions["ghost"]  # The ghost that is currently moving
    goal = positions["pacman"]  # Pac-Man's position
    other_ghosts = set(positions["ghosts"])  # Other ghosts' positions

    pq = [(0, start)]  # Priority queue (cost, position)
    visited = set()  # Use set for fast lookup
    parent = {start: None}
    cost_so_far = {start: 0}

    expanded_nodes = 0  # Count expanded nodes
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Track execution time

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

            execution_time = time.time() - start_time  # Compute elapsed time
            memory_usage = tracemalloc.get_traced_memory()[1]  # Peak memory usage
            tracemalloc.stop()

            return path[::-1][0] if path else start, expanded_nodes, memory_usage

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # Left → Up → Right → Down
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + map_state[next_pos[1]][next_pos[0]]

            if next_pos in other_ghosts and map_state[next_pos[1]][next_pos[0]] == float('inf'): 
                continue

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                heapq.heappush(pq, (new_cost, next_pos))
                parent[next_pos] = current
                cost_so_far[next_pos] = new_cost

    execution_time = time.time() - start_time  # Compute elapsed time
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return (-1, -1), expanded_nodes, memory_usage  # No path found
    
def astar_algorithm(map_state, positions):
    start = positions["ghost"]
    goal = positions["pacman"]
    other_ghosts = set(positions["ghosts"])

    pq = [(0, start)]
    parent = {}
    cost_so_far = {start: 0}

    expanded_nodes = 0
    tracemalloc.start()
    start_time = time.time()

    while pq:
        cost, current = heapq.heappop(pq)
        expanded_nodes += 1

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]

            execution_time = time.time() - start_time
            memory_usage = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            return path[::-1][0] if path else start, expanded_nodes, memory_usage
        
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + 1

            if next_pos in other_ghosts and map_state[next_pos[0]][next_pos[1]] != 0: 
                continue

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + abs(goal[0] - next_pos[0]) + abs(goal[1] - next_pos[1])
                heapq.heappush(pq, (priority, next_pos))
                parent[next_pos] = current

    execution_time = time.time() - start_time
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return (-1, -1), expanded_nodes, memory_usage
