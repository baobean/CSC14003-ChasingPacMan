import csv
import numpy as np
import timeit
from search import ucs_algorithm, bfs_algorithm

def load_test_map(file_path):
    """Load test map from CSV"""
    map_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            map_data.append([int(cell) for cell in row])
    return map_data

def assign_weights(map_data, pacman_pos, ghost_pos):
    """Create a weighted map ensuring Pacman and Ghost are placed correctly."""
    weight_map = []
    rows, cols = len(map_data), len(map_data[0])

    for i in range(rows):
        weight_row = []
        for j in range(cols):
            cell = map_data[i][j]

            # ✅ Ensure Pacman and Ghost are placed correctly
            if (i, j) == pacman_pos:
                weight_row.append(-10)  # Strong attraction for ghost
                continue
            elif (i, j) == ghost_pos:
                weight_row.append(0)  # Ghost's starting position
                continue

            if cell == 1:  # Wall (Not walkable)
                weight_row.append(float('inf'))
            elif cell == 0:  # Walkable Path
                weight = 1  # Default weight

                # ✅ Prefer open straight paths (reduce cost)
                if (0 < i < rows - 1 and map_data[i - 1][j] == 0 and map_data[i + 1][j] == 0) or \
                   (0 < j < cols - 1 and map_data[i][j - 1] == 0 and map_data[i][j + 1] == 0):
                    weight = 0.5  # Make straight paths attractive
                
                # ✅ Slightly increase cost for paths next to walls (to avoid hugging walls)
                adjacent_walls = 0
                if i > 0 and map_data[i - 1][j] == 1: adjacent_walls += 1
                if i < rows - 1 and map_data[i + 1][j] == 1: adjacent_walls += 1
                if j > 0 and map_data[i][j - 1] == 1: adjacent_walls += 1
                if j < cols - 1 and map_data[i][j + 1] == 1: adjacent_walls += 1
                
                if adjacent_walls >= 2:
                    weight = 1.0  # Slight penalty for corner/hugging walls
                
                weight_row.append(weight)
            elif cell == 5:  # Power Pellet
                weight_row.append(10)  # Ghost should avoid Power Pellets
            else:
                weight_row.append(1)  # Default case

        weight_map.append(weight_row)

    return np.array(weight_map)


# Load test map


# Define 5 test cases
test_cases = [
    {"pacman": (8,1), "ghost": (5,5)},
    {"pacman": (2,8), "ghost": (7,7)},
    {"pacman": (3,3), "ghost": (1,1)},
    {"pacman": (8,8), "ghost": (2,2)},
    {"pacman": (5,1), "ghost": (7,5)}
]

print("\n====== UCS Algorithm - Multiple Test Cases ======\n")


# Run UCS on each test case
for i, positions in enumerate(test_cases, start=1):
    pacman_pos = positions["pacman"]
    ghost_pos = positions["ghost"]
    test_map = load_test_map("source/map.csv")
    test_map = assign_weights(test_map, pacman_pos, ghost_pos)
    print(test_map)
    positions["ghosts"] = [(-1,-1)]  # Other ghosts are ignored

    print(f"Test Case {i}:")
    print(f"  Orange Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    test_number = 5000
    execution_time = timeit.timeit(lambda: bfs_algorithm(test_map, positions), number = test_number) / test_number
    next_move, expanded_nodes, memory_usage = bfs_algorithm(test_map, positions)

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Search Time: {execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f"  ➤ Number of Expanded Nodes: {expanded_nodes}")
    print("-" * 50)
