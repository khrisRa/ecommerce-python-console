import os
import elib
import subscipher
import sqlite3
import time
import mask
import sys
    
if os.path.exists("ecom.db"):
    elib.db_check()
else:
    elib.tbcreator()
    

while True:
    print("""
        Welcome to the MOB Retail Store
        1. if you want to Sign Up
        2. if you want to Login 
        3. if you want to Exit and Backup
    """)
    accOrLog = input("Please enter your choice: ")

    if accOrLog == "1":
        try:
            fieldstrip = subscipher.remove(input("Enter account email to add: "))
            uname = subscipher.check_email(fieldstrip)
            pwd = subscipher.check_pass(mask.getpass(prompt="Enter account password to add (letters and numbers only): ", mask='*'))
            encrypted = subscipher.encrypt(pwd)
            access = '0'
            acs = 'U'
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE LOGIN=?", [uname])
            conn.close

            if c.fetchone():
                print("Username already exists, please try again with different username")
            else:
                c.execute("INSERT INTO user(LOGIN, CRYPT_PASS, ACCESS_COUNT, ACS) VALUES (?, ?, ?, ?)", [uname, encrypted, access, acs])
                conn.commit()
                conn.close()
                print("Account added")
        except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again")
                sys.exit()
        except sqlite3.IntegrityError as e:
            print(e)
            break
        except FileNotFoundError:
            print("file not existent closing in 5secs \nplease wait...")
            time.sleep(5)
            sys.exit()
        except PermissionError:
            print("file in use on your system process")
            time.sleep(3)
            sys.exit()
    elif accOrLog == "2":
        try:
            uname = subscipher.remove(input("Enter username: ")).strip()
            pwd = mask.getpass(prompt="Enter password: ", mask='*')
            encrypted = subscipher.encrypt(pwd)
            acs = 'U'
            conn = sqlite3.connect("ecom.db")
            c = conn.cursor()

            c.execute("SELECT * FROM user WHERE LOGIN=? and CRYPT_PASS=?", [uname, encrypted])

            if c.fetchone() is None:
                print("Incorrect credentials, please verify username and password and try again")
            else:
                subscipher.UA(uname, acs)
        except sqlite3.OperationalError as e:
                print(e)
                print("Database might be locked check and run again")
                sys.exit()
        except sqlite3.IntegrityError as e:
            print(e)
            time.sleep(5)
            break
        except FileNotFoundError:
            print("file not existent closing in 5secs \nplease wait...")
            time.sleep(5)
            sys.exit()
        except PermissionError:
            print("file in use on your system process")
            time.sleep(3)
            sys.exit()

    elif accOrLog == "3":
        elib.backup()
        print("Good Bye closing in 5secs")
        time.sleep(5)
        break
    else:
        print("You have to press 1 or 2 or 3")