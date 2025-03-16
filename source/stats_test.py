import csv
import numpy as np
import timeit
from search import bfs_algorithm, ids_algorithm, ucs_algorithm, astar_algorithm
import wall

def load_test_map(file_path):
    """Load test map from CSV"""
    map_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            map_data.append([int(cell) for cell in row])
    return np.array(map_data)

def assign_weights(map_data, pacman_pos):
    """Assign pathfinding weights to the map."""
    rows, cols = map_data.shape
    weight_map = np.zeros((rows, cols))  # Create a NumPy array for weights
    for i in range(rows):
        for j in range(cols):
            cell = map_data[i][j]

            # ✅ Ensure correct placement of Pac-Man & Ghosts
            if (i, j) == pacman_pos:
                weight_map[i][j] = 0  # Pac-Man's target position
            # elif (i, j) in ghost_positions:
            #     weight_map[i][j] = 0  # Ghost starting positions
            elif cell in wall.wall_types:  # Walls
                weight_map[i][j] = float('inf')
            elif cell == 0:  # Walkable paths
                weight = 1  # Default cost

                # Reduce cost for straight paths to encourage open movement
                if (0 < i < rows - 1 and map_data[i - 1][j] == 0 and map_data[i + 1][j] == 0) or \
                    (0 < j < cols - 1 and map_data[i][j - 1] == 0 and map_data[i][j + 1] == 0):
                    weight = 0.5  # Straight paths are more attractive

                # Slightly increase cost near walls (to prevent hugging)
                adjacent_walls = sum([
                    1 if i > 0 and map_data[i - 1][j] == 1 else 0,
                    1 if i < rows - 1 and map_data[i + 1][j] == 1 else 0,
                    1 if j > 0 and map_data[i][j - 1] == 1 else 0,
                    1 if j < cols - 1 and map_data[i][j + 1] == 1 else 0
                ])

                if adjacent_walls >= 2:
                    weight = 1.0  # Small penalty for hugging corners

                weight_map[i][j] = weight
            else:
                weight_map[i][j] = 1  # Default cost

    return weight_map

# Define 5 test cases
test_cases = [    
    {"pacman": (1, 1), "ghost": (7, 1)},
    {"pacman": (1, 1), "ghost": (10, 23)},
    {"pacman": (1, 1), "ghost": (26, 1)},
    {"pacman": (1, 1), "ghost": (1, 20)},
    {"pacman": (1, 1), "ghost": (3, 26)}
]

print("\n====== BFS Algorithm - Multiple Test Cases ======\n")
# Run BFS on each test case
for i, positions in enumerate(test_cases, start=1):
    pacman_pos = positions["pacman"]
    ghost_pos = positions["ghost"]
    test_map = load_test_map("assets/map.csv")
    test_map = assign_weights(test_map, pacman_pos)
    positions["ghosts"] = [(-1,-1)]  # Other ghosts are ignored

    print(f"Test Case {i}:")
    print(f"  Blue Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    test_number = 5000
    execution_time = timeit.timeit(lambda: bfs_algorithm(test_map, positions), number = test_number) / test_number
    next_move, expanded_nodes, memory_usage = bfs_algorithm(test_map, positions)

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Search Time: {execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f"  ➤ Number of Expanded Nodes: {expanded_nodes}")
    print("-" * 50)

print("\n====== IDS Algorithm - Multiple Test Cases ======\n")
# Run IDS on each test case
for i, positions in enumerate(test_cases, start=1):
    pacman_pos = positions["pacman"]
    ghost_pos = positions["ghost"]
    test_map = load_test_map("assets/map.csv")
    test_map = assign_weights(test_map, pacman_pos)
    positions["ghosts"] = [(-1,-1)]  # Other ghosts are ignored

    print(f"Test Case {i}:")
    print(f"  Pink Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    test_number = 5000
    execution_time = timeit.timeit(lambda: ids_algorithm(test_map, positions), number = test_number) / test_number
    next_move, expanded_nodes, memory_usage = ids_algorithm(test_map, positions)

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Search Time: {execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f"  ➤ Number of Expanded Nodes: {expanded_nodes}")
    print("-" * 50)

print("\n====== UCS Algorithm - Multiple Test Cases ======\n")
# Run UCS on each test case
for i, positions in enumerate(test_cases, start=1):
    pacman_pos = positions["pacman"]
    ghost_pos = positions["ghost"]
    test_map = load_test_map("assets/map.csv")
    test_map = assign_weights(test_map, pacman_pos)
    positions["ghosts"] = [(-1,-1)]  # Other ghosts are ignored

    print(f"Test Case {i}:")
    print(f"  Orange Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    test_number = 5000
    execution_time = timeit.timeit(lambda: ucs_algorithm(test_map, positions), number = test_number) / test_number
    next_move, expanded_nodes, memory_usage = ucs_algorithm(test_map, positions)

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Search Time: {execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f"  ➤ Number of Expanded Nodes: {expanded_nodes}")
    print("-" * 50)

print("\n====== A-Star Algorithm - Multiple Test Cases ======\n")
# Run A-Star on each test case
for i, positions in enumerate(test_cases, start=1):
    pacman_pos = positions["pacman"]
    ghost_pos = positions["ghost"]
    test_map = load_test_map("assets/map.csv")
    test_map = assign_weights(test_map, pacman_pos)
    positions["ghosts"] = [(-1,-1)]  # Other ghosts are ignored

    print(f"Test Case {i}:")
    print(f"  Red Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    test_number = 5000
    execution_time = timeit.timeit(lambda: astar_algorithm(test_map, positions), number = test_number) / test_number
    next_move, expanded_nodes, memory_usage = astar_algorithm(test_map, positions)

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Search Time: {execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f"  ➤ Number of Expanded Nodes: {expanded_nodes}")
    print("-" * 50)
