import csv
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

# Load test map
test_map = load_test_map("source/map.csv")

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
