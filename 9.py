from itertools import permutations

n = int(input("Enter number of cities: "))
g = []

print("Enter cost matrix:")
for i in range(n):
    g.append(list(map(int, input().split())))

cities = list(range(1, n))
mc = float('inf')
path = []

for p in permutations(cities):
    cost = g[0][p[0]]
    for i in range(len(p) - 1):
        cost += g[p[i]][p[i + 1]]
    cost += g[p[-1]][0]

    if cost < mc:
        mc = cost
        path = (0,) + p + (0,)

print("Minimum Cost:", mc)
print("Path:", " -> ".join(map(lambda x: str(x + 1), path)))
