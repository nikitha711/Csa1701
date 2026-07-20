from collections import deque

goal = (1,2,3,4,5,6,7,8,0)

def bfs(start):
    q = deque([[start]])
    visited = {start}

    while q:
        path = q.popleft()
        s = path[-1]

        if s == goal:
            return path

        i = s.index(0)
        for j in [i-3, i+3, i-1, i+1]:
            if 0 <= j < 9 and abs(i%3 - j%3) + abs(i//3 - j//3) == 1:
                t = list(s)
                t[i], t[j] = t[j], t[i]
                t = tuple(t)
                if t not in visited:
                    visited.add(t)
                    q.append(path + [t])

start = tuple(map(int, input("Enter 9 numbers: ").split()))

ans = bfs(start)

for state in ans:
    print(state[:3])
    print(state[3:6])
    print(state[6:])
    print()
