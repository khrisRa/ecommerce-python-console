import sqlite3
import re
import sys
import time
import datetime



##tables creator
def tbcreator():
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE user
                    ("USER_ID"	INTEGER NOT NULL,
            "LOGIN"	TEXT NOT NULL UNIQUE,
            "CRYPT_PASS"	TEXT NOT NULL,
            "ACCESS_COUNT"	INTEGER NOT NULL,
            "ACS" TEXT NOT NULL,
            PRIMARY KEY("USER_ID" AUTOINCREMENT))''')
        c.execute('''CREATE TABLE products
                    ("P_ID"	INTEGER NOT NULL,
            "desc"	TEXT NOT NULL UNIQUE,
            "price"	FLOAT NOT NULL,
            "tag"	TEXT NOT NULL,
            "qty" INTEGER NOT NULL,
            PRIMARY KEY("P_ID" AUTOINCREMENT))''')
        c.execute('''CREATE TABLE cart
                    ("C_ID"	INTEGER NOT NULL,
            "LOGIN"	TEXT NOT NULL,        
            "desc"	TEXT NOT NULL,
            "price"	FLOAT NOT NULL,
            "tag"	TEXT NOT NULL,
            "qty" INTEGER NOT NULL,
            "status"	TEXT NOT NULL,
            "date"	TEXT NOT NULL,
            PRIMARY KEY("C_ID" AUTOINCREMENT))''')
        c.execute("INSERT INTO user(LOGIN, CRYPT_PASS, ACCESS_COUNT, ACS) VALUES ('admin', 'tecsg', '0', 'A' )")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
    except PermissionError:
        print("file in use on your system process")
    
    
def hme_pg():
        print("""
        Welcome to the MOB Retail Store
            1. Search Products
            2. Buy
            3. Your Cart
            4. Logout
        """)


##Encryption and decryption
def encrypt(txt):
    x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    y = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    table = str.maketrans(x, y)
    transl = txt.translate(table)
    return transl


def decrypt(txt):
    x = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    y = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    table = str.maketrans(x, y)
    transl = txt.translate(table)
    return transl


def db_check():
    conn = sqlite3.connect("ecom.db", timeout=1)
    c = conn.cursor()
    try:
        c.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", ['admin'])
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()


def remove(string):
    unamestrip = string.replace(" ", "")
    return unamestrip


def check_pass(pwd):
    pattern = "^[A-Za-z0-9]*$"
    while not re.match(pattern, pwd):
        pwd = input("Enter account password to add (letters and numbers only): ")
    else:
        pass
    return pwd


def tag_check(tag):
    pattern = "^[A-Za-z]*$"
    while not re.match(pattern, tag):
        tag = input("Enter Tag category (One Word with letters only): ")
    else:
        pass
    return tag


def check_email(uname):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    while not re.fullmatch(regex, uname):
        uname = input("Invalid email please check entry Enter account email to add: ")

    else:
        pass
    return uname


def check_in(twd):
    pattern = "^[0-9]*$"
    while not re.match(pattern, twd):
        twd = input("Enter account number (numbers): ")
    else:
        pass
    return twd


def check_amt(twd):
    pattern = "^[0-9.]*$"
    while not re.match(pattern, twd):
        twd = input("Enter amount up to two decimal places (numbers): ")
    else:
        pass
    return twd


def create_prd(desc):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products WHERE desc=?", [desc])
        if c.fetchone():
            print("Product Description already exists, please try again with different Description \nOr use Search function to update an existing product \nplease wait...")
            time.sleep(2)
        else:
            price = check_amt(input("Enter product price:-->"))
            cat = tag_check(remove(input("Enter product category tag:-->")))
            tag = cat.upper()
            qty = check_in(input("Enter product qty available:-->"))
            c.execute("INSERT INTO products(desc, price, tag, qty) VALUES (?, ?, ?, ?)", [desc, price, tag, qty])
            conn.commit()
            conn.close()
            print("Product: "+desc+"\nCreation successfull \nplease wait...")
            time.sleep(2)
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
        print("This product already exists")
        sys.exit()
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(5)
        sys.exit()
    except PermissionError:
        print("file in use on your system process")
        sys.exit()
        
        
def search():
    while True:
        print("""
            Search By Tag or Description
            Tags are products categories for example: SHOES/VEG/FRUITS/CLOTHING
                1. Tag
                2. Description
                3. Back
            """)
        s_choice = input("Please enter desired operation: ")
        if s_choice == "1":
            wrd = input("Enter tag description: ")
            word = wrd.lstrip()
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()
            try:
                c.execute("SELECT desc, price, tag FROM products WHERE tag LIKE ?", (['%'+word+'%']))
                record = c.fetchall()
                for row in record:
                    print(
                    'Product Description:- ', row[0], "\n"
                    'Price:- ', row[1], "\n"
                    'Category:- ', row[2], "\n"
                    )
                    conn.close()
                else:
                    print("No more results/End of results")
                conn.close()
                time.sleep(3)
            except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again")
                sys.exit()
            except sqlite3.IntegrityError as e:
                print(e)
                sys.exit()
            except FileNotFoundError:
                print("file not existent closing in 5secs \nplease wait...")
                time.sleep(5)
                sys.exit()
            except PermissionError:
                print("file in use on your system process")
                time.sleep(3)
                sys.exit()
        elif s_choice == "2":
            wrd = input("Enter Product description: ")
            word = wrd.lstrip()
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()
            try:
                c.execute("SELECT desc, price, tag FROM products WHERE desc LIKE ?", (['%'+word+'%']))
                record = c.fetchall()
                for row in record:
                    print(
                    'Product Description:- ', row[0], "\n"
                    'Price:- ', row[1], "\n"
                    'Category:- ', row[2], "\n"
                    )
                    conn.close()
                else:
                    print("No more results/End of results \nplease wait...")
                conn.close()
                time.sleep(3)
            except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again \nplease wait...")
                sys.exit()
            except sqlite3.IntegrityError as e:
                print(e)
            except FileNotFoundError:
                print("file not existent closing in 5secs \nplease wait...")
                time.sleep(5)
                sys.exit()
            except PermissionError:
                print("file in use on your system process \nplease wait...")
                time.sleep(3)
                sys.exit()
        elif s_choice == "3":
            break
        else:
            print("You have to press 1 or 2 or 3")  


def backup():
    try:
        conn = sqlite3.connect("ecom.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user")
        results = c.fetchall()
        headers = [i[0] for i in c.description]
        import csv

        csvfile = csv.writer(open('userbckup.csv', 'w', newline=''),
                             delimiter=',', lineterminator='\r\n',
                             quoting=csv.QUOTE_ALL, escapechar='\\')
        csvfile.writerow(headers)
        csvfile.writerows(results)
        print("backup success")
        conn.close()
    except sqlite3.DatabaseError as e:
        print(e)
        print("backup unsuccessful")
    except PermissionError as w:
        print(w)
        print("backup unsuccessful")
        print("Check if the file is already open")
        
        
def update_prd(desc):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products WHERE desc=?", [desc])
        if c.fetchone():
            print("Enter New Details Below: ")
            des = input("Enter product description:-->")
            prd = des.lstrip().capitalize()
            price = check_amt(input("Enter product price:-->"))
            cat = tag_check(remove(input("Enter product category tag:-->")))
            tag = cat.upper()
            qty = check_in(input("Enter product qty available:-->"))
            c.execute("UPDATE products SET desc = ?, price = ?, tag = ?, qty = ? WHERE desc = ?", [prd, price, tag, qty, desc])
            conn.commit()
            conn.close()
            print("Product: "+desc+"\nUpdate successfull \nplease wait...")
            time.sleep(2)
        else:
            print("Product does not exist, verify or search before updating...")
            time.sleep(2)
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(5)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
        
        
def del_prd(desc):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products WHERE desc=?", [desc])
        if c.fetchone():
            c.execute("DELETE FROM products WHERE desc = ?", [desc])
            conn.commit()
            conn.close()
            print("Product: " + desc + "\nDelete successfull \nplease wait...")
            time.sleep(2)
        else:
            print("Product: " + desc + "\ndoes not exist, verify or search before deleting...")
            time.sleep(2)
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(5)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
        
        
def buy_prd(desc, uname):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute("SELECT desc, price, tag FROM products WHERE desc=?", [desc])
        if c.fetchone():
            dis_item(desc)
            qty = check_in(input("Enter qty desired:-->"))
            c.execute("SELECT desc, price, tag FROM products WHERE desc=? AND qty = ?", [desc, qty])
            if c.fetchone():
                print("Product out of stock\nplease try again later")
                time.sleep(2)
            else:
                # usr = c.execute("SELECT LOGIN FROM user WHERE LOGIN=?", [uname])
                c.execute("SELECT price, tag FROM products WHERE desc=?", [desc])
                rec = c.fetchone()
                pr = rec[0]
                tg = rec[1]
                dt = datetime.datetime.now()
                st = 'O'
                c.execute("UPDATE products SET qty = qty - ? WHERE desc =?", [qty, desc])
                c.execute("INSERT INTO cart(LOGIN, desc, price, tag, qty, status, date) VALUES (?, ?, ?, ?, ?, ?, ?)", [uname, desc, pr, tg, qty, st, dt])
                conn.commit()
                conn.close()
                print("Product: " + desc + "\nAdded to Cart \nplease wait...")
                time.sleep(2)
        else:
            print("Product does not exist, verify or search before buying...")
            time.sleep(2)
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(3)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
        
        
def dis_item(desc):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:   
             
        c.execute("SELECT desc, price, tag FROM products WHERE desc=?", [desc])
        record = c.fetchall()
        for row in record:
            print(
                '\nProduct Description:- ', row[0], "\n"
                'Price:- ', row[1], "\n"
                )
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(3)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
        
        
def crt_updt(desc):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    so = 'O'
    try:
             
        c.execute("SELECT desc, price, qty FROM cart WHERE desc=? AND status = ?", [desc, so])
        record = c.fetchall()
        for row in record:
            print(
                '\nProduct Description:- ', row[0], "\n"
                'Price:- ', row[1], "\n"
                'Qty:- ', row[2], "\n"
                )
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(3)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
        
        
def dis_cart(uname):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:        
        st = 'O'
        c.execute("SELECT desc, price, qty FROM cart WHERE LOGIN = ? AND status = ?", [uname, st])
        record = c.fetchall()
        for row in record:
            print(
                '\nProduct Description:- ', row[0], "\n"
                'Price:- ', row[1], "\n"
                'Qty:- ', row[2], "\n"
                'Total:- ', round((row[1]*row[2]), 2), "\n"
                )
        else:
            c.execute("SELECT SUM(price*qty) FROM cart WHERE LOGIN = ? AND status = ?", [uname, st])
            result = c.fetchone()
            rslt =str(round(result[0], 2))
            print("Cart Grand Total: " + rslt)
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(3)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
    
        
        
def cart(uname):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()  
    try:
        st = 'O'
        c.execute("SELECT desc, price, qty FROM cart WHERE LOGIN = ? AND status = ?", [uname, st])
        if c.fetchall():
            dis_cart(uname)
            checkout(uname)
        else:
            print("Your cart is empty")            
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again \nplease wait...")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
        time.sleep(3)
        sys.exit()
    except PermissionError:
        print("file in use on your system process \nplease wait...")
        time.sleep(3)
        sys.exit()
                
                
def checkout(uname):
    while True:
        print("""
                1. Checkout
                2. Modify Cart
                3. Back
        """)
        ch = input("Enter Your Choice: ")
        st = 'C'
        so = 'O'
        dt = datetime.datetime.now()
        if ch == "1":
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()  
            try:
                c.execute("UPDATE cart SET status = ?, date = ? WHERE LOGIN = ? and status = ?", [st, dt, uname, so])
                conn.commit()
                conn.close()
                print("Checked out successfully \nplease wait...")
                time.sleep(2)
                break
            except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again \nplease wait...")
                sys.exit()
            except sqlite3.IntegrityError as e:
                print(e)
            except FileNotFoundError:
                print("file not existent closing in 5secs \nplease wait...")
                time.sleep(5)
                sys.exit()
            except PermissionError:
                print("file in use on your system process \nplease wait...")
                time.sleep(3)
                sys.exit()
        elif ch == "2":
            des = input("Enter product description from cart to modify:-->")
            prd = des.lstrip().capitalize()
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM cart WHERE desc=? AND status = ? AND LOGIN = ?", [prd, so, uname])
                if c.fetchone():
                    crt_updt(prd)
                    qty = check_in(input("Enter New qty:-->"))
                    if qty == '0':
                        c.execute("DELETE FROM cart WHERE desc=? AND status = ? AND LOGIN = ?", [prd, so, uname])
                        conn.commit()
                        conn.close()
                        print("Product: " + prd + "\nRemoved successfully \nplease wait...")
                        time.sleep(2)
                        cart(uname)
                    else:
                        c.execute("UPDATE cart SET qty = ? WHERE desc=? AND status = ? AND LOGIN = ?", [qty, prd, so, uname])
                        conn.commit()
                        conn.close()
                        print("Product: " + prd + "\nUpdate successfull \nplease wait...")
                        time.sleep(2)
                        cart(uname)
                else:
                    print("this item is not in your cart please verify again")
            except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again \nplease wait...")
                sys.exit()
            except sqlite3.IntegrityError as e:
                print(e)
            except FileNotFoundError:
                print("file not existent closing in 5secs \nplease wait...")
                time.sleep(3)
                sys.exit()
            except PermissionError:
                print("file in use on your system process \nplease wait...")
                time.sleep(3)
                sys.exit()
        elif ch == "3":
            break
        else:
            print("You have to press 1 or 2 or 3")   
           