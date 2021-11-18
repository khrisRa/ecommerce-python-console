import elib
import time
import sys
import subscipher


def usr_hme():
    while True:
        elib.hme_pg()
        choice = input("Please enter desired operation: ")
        if choice == "1":
            elib.search()
        elif choice == "2":
            des = input("Enter product description:-->")
            prd = des.lstrip().capitalize()
            usr = subscipher.usr
            elib.buy_prd(prd,usr)
        elif choice == "3":
            usr = subscipher.usr
            elib.cart(usr)
        elif choice == "4":
            print("Good Bye closing in 5secs")
            time.sleep(5)
            sys.exit()
        else:
            print("You have to press 1 or 2 or 3 or 4")
