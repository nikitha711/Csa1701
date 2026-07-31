# Tic Tac Toe

b = [' '] * 9

def show():
    print(f"{b[0]}|{b[1]}|{b[2]}")
    print("-+-+-")
    print(f"{b[3]}|{b[4]}|{b[5]}")
    print("-+-+-")
    print(f"{b[6]}|{b[7]}|{b[8]}")

def win(p):
    w = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(b[x]==b[y]==b[z]==p for x,y,z in w)

for i in range(9):
    show()
    p = 'X' if i % 2 == 0 else 'O'
    pos = int(input(f"{p} position (1-9): ")) - 1
    if b[pos] == ' ':
        b[pos] = p
        if win(p):
            show()
            print(p, "Wins!")
            break
    else:
        print("Invalid Move")
        break
else:
    show()
    print("Match Draw")
