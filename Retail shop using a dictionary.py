# ============================================================
#  BREVINE RETAIL SHOP
#  Version 1 — with while loop, list and log in
#  By: Brevine Oduor Osoro
# ============================================================
import getpass
attempts=0
while attempts <3:
    print( "WELCOME TO  BREVINE RETAIL SHOP")
    print("Admin Log In Only")
    User=input("USER NAME: ")
    Password= getpass.getpass("PASSWORD: ")
    Shop={ "Rice":120, "Sugar":150, "Tea Leaves":10, "Milk":60, "Choco":20}
    if User=="BREVINE" and Password == "526.kqa":
        print("LOG IN SUCCESSFUL WELCOME BACK TO SESSION.")
        print( "ITEMS         UNIT  PRICE")
        for a,b in Shop.items():
            print(a ,"        ", b)
        print(" Please enter quantity of items purchased. NOT PURCHASED please enter Zero")
        total=0
        count=0
        total_qty=0
        for a,b in Shop. items():
            qty=int(input("Quantity of "+ a +":  "))
            if qty>0:
                count+=1
                total_qty=total_qty+qty
            total= total+ (qty*b)
        print("Your Amount is: ", total,".00")
        print("Total items purchased is: ", count)
        print ("Total pieces purchased is: ", total_qty)
        if total >400:
               print("Total Bill is ", total,".00")
               print("CONGRATULATIONS YOU HAVE RECIEVED 10 PERCENT DISCOUNT ")
               U=total-total*float(0.1)
               print( "Your New Bill: ", U)
        else:
                print("SORRY YOU MISSED DISCOUNT. SHOP ABOVE 400 NEXT TIME TO GET 10 PERCENT DISCOUNT")
                print(" Your Bill is ", total)
             
        break
    else:
         attempts+=1
         remaining=3-attempts
         if remaining>0:
             print("WRONG DETAILS PLEASE TRY AGAIN")
             print("Remaing attempts", remaining)
         if attempts ==3:
             print( "System locked.please contact admin")
             break
         