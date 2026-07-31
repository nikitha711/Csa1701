# Vacuum Cleaner Problem

A = input("Room A (clean/dirty): ").lower()
B = input("Room B (clean/dirty): ").lower()

if A == "dirty":
    print("Cleaning Room A")
    A = "clean"

if B == "dirty":
    print("Cleaning Room B")
    B = "clean"

print("Final State:")
print("Room A:", A)
print("Room B:", B)
