from collections import deque
import heapq

def bfs_algorithm(map_state, positions):
    return (-1, -1)  # No path found

def dfs_algorithm(map_state, positions):
    return (-1, -1)

def ucs_algorithm(map_state, positions):
    """Uniform-Cost Search for a specific ghost, avoiding other ghosts"""
    
    start = positions["ghost"]  # The ghost that is currently moving
    goal = positions["pacman"]  # Pac-Man's position
    other_ghosts = set(positions["ghosts"])  # All ghosts' positions except the current one

    pq = [(0, start)]  # Priority queue: (cost, position)
    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    while pq:
        cost, current = heapq.heappop(pq)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            return path[::-1][0] if path else start  # Return the next move

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)

            # Avoid walls and other ghosts
            if next_pos not in visited and map_state[next_pos[1]][next_pos[0]] == 0 and next_pos not in other_ghosts:
                heapq.heappush(pq, (cost_so_far[current] + 1, next_pos))
                visited.add(next_pos)
                parent[next_pos] = current
                cost_so_far[next_pos] = cost_so_far[current] + 1

    return (-1, -1)  # No path found


def astar_algorithm(map_state, positions):
    return (-1, -1)
