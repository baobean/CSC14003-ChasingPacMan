import csv
import time
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

    total_execution_time = 0
    total_memory_usage = 0
    step_count = 0

    print(f"Test Case {i}:")
    print(f"  Orange Ghost Starting Position: {positions['ghost']}")
    print(f"  Pac-Man Position: {positions['pacman']}")

    while positions["ghost"] != positions["pacman"]:
        next_move, execution_time, _, memory_usage = bfs_algorithm(test_map, positions)

        if next_move == (-1, -1):  
            print("No path found!")
            break  

        positions["ghost"] = next_move  
        total_execution_time += execution_time
        total_memory_usage += memory_usage
        step_count += 1

        print(f"  Step {step_count}: Ghost moves to {next_move}")

    print(f"\n  Final Results for Test Case {i}:")
    print(f"  ➤ Total Execution Time: {total_execution_time:.6f} seconds")
    print(f"  ➤ Total Memory Usage: {total_memory_usage / 1024:.2f} KB")
    print(f"  ➤ Total Steps Taken: {step_count}")
    print("-" * 50)
