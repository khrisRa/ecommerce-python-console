import sqlite3
import re
import sys
import Homepage
import admin
import mask

usr = ""


def session(uname):
    global usr
    usr = uname
    return usr


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


def remove(string):
    unamestrip = string.replace(" ", "")
    return unamestrip


def check_pass(pwd):
    pattern = "^[A-Za-z0-9]*$"
    while not re.match(pattern, pwd):
        pwd = mask.getpass(prompt="Enter account password to add (letters and numbers only): ", mask='*')
    else:
        pass
    return pwd


def check_email(uname):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    while not re.fullmatch(regex, uname):
        uname = input("Invalid email please check entry Enter account email to add: ")

    else:
        pass
    return uname
       
        
def UA(uname, acs):
    conn = sqlite3.connect("ecom.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM user WHERE LOGIN=? and ACS=?", [uname, acs])
        if c.fetchone():
            c.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", [uname])
            conn.commit()
            conn.close()
            print("Logged in!")
            session(uname)
            Homepage.usr_hme()            
        else:
            c.execute("SELECT * FROM user WHERE LOGIN=? and ACS!=?", [uname, acs])
            if c.fetchone():
                c.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", [uname])
                conn.commit()
                conn.close()
                print("Logged in!")
                admin.admin()            
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()
    except sqlite3.IntegrityError as e:
        print(e)
        print("This product already exists")
    except FileNotFoundError:
        print("file not existent closing in 5secs \nplease wait...")
    except PermissionError:
        print("file in use on your system process")
    
