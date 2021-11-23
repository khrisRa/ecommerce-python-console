import os
import elib
import sys
import time

        
if os.path.exists("ecom.db"):
    elib.db_check()
else:
    elib.tbcreator()
    
    
def admin():   
    while True:
        print("""
                Welcome ADMIN MOB Shop
                1. Search Products
                2. Create products
                3. Update products
                4. Delete products
                5. Order history
                6. Logout
            """)
        choice = input("Please enter desired operation: ")
        if choice == "1":
            elib.search()
        elif choice == "2":
            des = input("Enter product description:-->")
            prd = des.lstrip().capitalize()
            elib.create_prd(prd)
        elif choice == "3":
            des = input("Enter product description:-->")
            prd = des.lstrip().capitalize()
            elib.update_prd(prd)
        elif choice == "4":
            des = input("Enter product description:-->")
            prd = des.lstrip().capitalize()
            elib.del_prd(prd)
        elif choice == "5":
            elib.a_orderhis()
        elif choice == "6":
            print("Good Bye closing in 5secs")
            elib.backup()
            time.sleep(5)
            sys.exit()
        else:
            print("You have to press 1 or 2 or 3 or 4 or 5")