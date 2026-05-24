while True:
    name = input("name")
    x = int(input ("first score"))
    y = int(input( " second score"))
    p = x*y 
    if p < 20:
        print (" less than avearge "+ name+ " try again")
    else:
        print (" good work procede to next class")
        break 