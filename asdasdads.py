matrix = [["Mange", 66],
          ["asdad", 22],
          ["Leo", 18],
          ["Deivids", 25]]


matrix.sort(key=lambda age: age[1], reverse=True)
print (matrix)

matrix.sort(key=lambda age: age[1])

test = ("\nasdasd", "Anne frank", "Hatler", "Frank\n")
test2 = ("asdasd", "Anne frank", "Hatler", "Frank")

print(" , ".join(test))
print(test2)

board = [[" "for _ in range(10)] for _ in range(10)]

for row in board:
    print(" I ".join(row))
    print("-" * 37)

my_string = ("Hej jag heter Leo")
length = len(my_string)
print(length)