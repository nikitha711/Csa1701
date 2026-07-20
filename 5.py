from collections import deque

def is_valid(m_left, c_left, m_right, c_right):
    if (m_left < 0 or c_left < 0 or
        m_right < 0 or c_right < 0):
        return False

    if m_left > 0 and c_left > m_left:
        return False

    if m_right > 0 and c_right > m_right:
        return False

    return True

def get_successors(state):
    m_left, c_left, boat = state
    successors = []

    moves = [(2,0), (0,2), (1,1), (1,0), (0,1)]

    for m, c in moves:
        if boat == 0:  
            new_state = (m_left - m, c_left - c, 1)
        else:          
            new_state = (m_left + m, c_left + c, 0)

        ml, cl, b = new_state
        mr = 3 - ml
        cr = 3 - cl

        if is_valid(ml, cl, mr, cr):
            successors.append(new_state)

    return successors


def bfs():
    start = (3, 3, 0)      
    goal = (0, 0, 1)

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        if state not in visited:
            visited.add(state)

            for next_state in get_successors(state):
                if next_state not in visited:
                    queue.append((next_state, path + [next_state]))

    return None

solution = bfs()

if solution:
    print("Solution Found:\n")
    print("ML CL Boat | MR CR")
    print("-------------------")

    for state in solution:
        ml, cl, boat = state
        mr = 3 - ml
        cr = 3 - cl
        boat_side = "Left" if boat == 0 else "Right"
        print(f"{ml}  {cl}  {boat_side:5} | {mr}  {cr}")
else:
    print("No solution found.")
