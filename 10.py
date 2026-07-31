from queue import PriorityQueue

graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 3), ('E', 1)],
    'C': [('F', 5)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

h = {'A': 4, 'B': 2, 'C': 4, 'D': 3, 'E': 1, 'F': 0}

start = input("Enter start node: ")
goal = input("Enter goal node: ")

pq = PriorityQueue()
pq.put((h[start], 0, start, [start]))
visited = set()

while not pq.empty():
    f, g, node, path = pq.get()

    if node == goal:
        print("Path:", " -> ".join(path))
        print("Cost:", g)
        break

    if node in visited:
        continue
    visited.add(node)

    for nxt, cost in graph[node]:
        if nxt not in visited:
            pq.put((g + cost + h[nxt], g + cost, nxt, path + [nxt]))
