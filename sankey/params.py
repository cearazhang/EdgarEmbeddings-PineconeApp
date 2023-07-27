print(1, 2, 3, 4, "hello", True, [4, 5, 6])
print(max(3, 42, 7, -5))

# * identifies vals with 2 must have vals <- positional parameter


def mysum(x, y, *vals):
    return x + y + sum(vals)


print(mysum(4, 5, 6, 7, 8, 10))