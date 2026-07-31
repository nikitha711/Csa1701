# Map Coloring using CSP

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

colors = ["Red", "Green", "Blue"]
result = {}

def solve(node):
    if node == len(graph):
        return True

    state = list(graph.keys())[node]

    for color in colors:
        if all(result.get(n) != color for n in graph[state]):
            result[state] = color
            if solve(node + 1):
                return True
            del result[state]
    return False

solve(0)

print("Map Coloring:")
for state, color in result.items():
    print(state, "->", color)
