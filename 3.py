from collections import deque

def water_jug(a, b, target):
    q = deque([(0, 0)])
    visited = set()

    while q:
        x, y = q.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        print((x, y))

        if x == target or y == target:
            print("Goal Reached")
            return

        q.extend([
            (a, y),
            (x, b),
            (0, y),
            (x, 0),
            (max(0, x-(b-y)), min(b, x+y)),
            (min(a, x+y), max(0, y-(a-x)))
        ])

a = int(input("Enter capacity of Jug A: "))
b = int(input("Enter capacity of Jug B: "))
target = int(input("Enter target amount: "))

water_jug(a, b, target)
