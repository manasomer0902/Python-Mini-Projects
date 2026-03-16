
# How to create reverse pyramid in python

def mid_reverse_pyramid(rows):
    for i in range(rows, 0, -1):
        for j in range(rows - i):
            print(" ", end = "")
        for j in range(2 * i - 1):
            print("*", end = "")
        print()

# number of rows in the mid-reverse-pyramid

num_rows = int(input("Enter the number of rows: "))
mid_reverse_pyramid(num_rows)
