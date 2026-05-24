while True:
    a = int(input("first number: "))
    b = int(input("second number: "))
    x = a + b
    if x < 10:
        print("invalid numbers!")
    else:
        print("valid! sum is", x)
        break