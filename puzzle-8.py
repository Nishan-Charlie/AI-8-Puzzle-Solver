from queue import Queue, PriorityQueue

MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}


def read_puzzle(file_name):
    try:
        with open(file_name, 'r') as file:
            puzzle = tuple(tuple(map(int, line.split())) for line in file)
            if len(puzzle) != 3 or any(len(row) != 3 for row in puzzle):
                raise ValueError("Invalid puzzle format: must be 3x3 grid of digits")
            return puzzle
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        exit()

def print_puzzle(puzzle):
    for row in puzzle:
        for number in row:
            print(number, end=' ')
        print()
    print()


from queue import Queue, PriorityQueue

def read_puzzle_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    puzzle = [[int(num) for num in line.split()] for line in lines]
    return puzzle

def get_children(puzzle):
    children = {}
    zero_row, zero_col = None, None
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                zero_row, zero_col = row, col
                break
        if zero_row is not None:
            break
    for d_row, d_col, move_name in [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]:
        new_row, new_col = zero_row + d_row, zero_col + d_col
        if 0 <= new_row < len(puzzle) and 0 <= new_col < len(puzzle[0]):
            new_puzzle = [row[:] for row in puzzle]
            new_puzzle[zero_row][zero_col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[zero_row][zero_col]
            children[move_name] = new_puzzle
    return children

def bfs(start_state, GOAL_STATE):
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    queue = Queue()
    queue.put((start_state, []))
    nodes_expanded = 0
    while not queue.empty():
        puzzle, path = queue.get()
        nodes_expanded += 1
        if puzzle == GOAL_STATE:
            return path, nodes_expanded
        for move_name, child in get_children(puzzle).items():
            if tuple(map(tuple, child)) not in visited:
                visited.add(tuple(map(tuple, child)))
                queue.put((child, path + [move_name]))
    return None, None

def misplaced_tiles(puzzle, goal_puzzle):
    return sum(puzzle[i][j] != goal_puzzle[i][j] for i in range(len(puzzle)) for j in range(len(puzzle[0])))

def best_first_search(start_state, goal_state, heuristic_function):
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    queue = PriorityQueue()
    queue.put((heuristic_function(start_state, goal_state), start_state, []))
    nodes_expanded = 0
    while not queue.empty():
        _, puzzle, path = queue.get()
        nodes_expanded += 1
        if puzzle == goal_state:
            return path, nodes_expanded
        for move_name, child in get_children(puzzle).items():
            if tuple(map(tuple, child)) not in visited:
                visited.add(tuple(map(tuple, child)))
                priority = heuristic_function(child, goal_state)
                queue.put((priority, child, path + [move_name]))
    return None, None


def print_results(path, length, nodes_expanded):
    print("Solution path:")
    for move_name in path:
        print(move_name)
    print(f"Length of path: {length}")
    print(f"Number of nodes expanded: {nodes_expanded}")


def main():
    # Prompt user for the name of the file containing the initial state
    filename = input("Please enter the name of the file containing the initial state of the puzzle: ")
    initial_state = read_puzzle(filename)
    print_puzzle(initial_state)
    # Prompt user to select an algorithm to use
    print("Please select which algorithm you would like to use:")
    print("1. Breadth-first search")
    print("2. Best-first search")
    algorithm_choice = input()

    # Validate the user's choice of algorithm
    if algorithm_choice not in ['1', '2']:
        print("Invalid choice of algorithm. Please select 1 or 2.")
        return

    # Select the appropriate algorithm based on user's choice
    if algorithm_choice == '1':
        search_algorithm = bfs
        algorithm_name = "breadth-first search"
    else:
        search_algorithm = best_first_search
        algorithm_name = "best-first search"

    # Set the goal state
    goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    # Solve the puzzle using the selected algorithm
    path, nodes_expanded = search_algorithm(initial_state, goal_state)
    # Print the results
    print(f"\nUsing {algorithm_name}:")
    if path is None:
        print("No solution found.")
    else:
        print(f"Solution path: {path}")
        print(f"Number of nodes expanded: {nodes_expanded}")
        print(f"Length of solution path: {len(path)}")


if __name__ == '__main__':
    main()
