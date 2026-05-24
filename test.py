# a = 5
# b = 3
# result = a | b
# print(result)   # 7

# name: str | None = None
# print(name)

# for i in range(10):
#     print(i, i%3, i//3)

dirrectionKeys = {i: (i, "up" if i%2 else "down", 10-(i-9)//2) for i in range(10, 28)}
# dirrectionKeys = {i: ("up" if i%2 else "down", (i-10)//2) for i in range(10, 28)}

for key in dirrectionKeys.values():
    print(*key)