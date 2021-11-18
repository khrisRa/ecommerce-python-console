import sqlite3
import time
import sys

conn = sqlite3.connect("ecom.db")
c = conn.cursor()
try:
    c.execute('''INSERT INTO products(desc, price, tag, qty) 
              VALUES 
              ('Apple', '2.99', 'FRUITS', '25' ),
              ('Pear', '2.99', 'FRUITS', '25' ),
              ('Orange', '2.99', 'FRUITS', '25' ),
              ('Canned beans', '1.99', 'CANNED', '25' ),
              ('Canned tomatoes', '1.99', 'CANNED', '25' ),
              ('Tuna', '1.17', 'CANNED', '25' ),
              ('Corn', '1.07', 'CANNED', '25' ),
              ('Rice', '13.99', 'GRAIN', '25' ),
              ('Cumin', '4.17', 'SPICE', '25' ),
              ('Coriander powder', '4.17', 'SPICE', '25' ),
              ('Curry leaves', '1.17', 'VEG', '25' ),
              ('Green onions', '1.17', 'VEG', '25' ),
              ('Cheerios', '4.44', 'CEREAL', '25' ),
              ('Weetabix', '4.44', 'CEREAL', '25' ),
              ('Air force2', '49.44', 'SHOES', '25' ),
              ('Nike shirt', '24.50', 'CLOTHING', '25' ),
              ('Garmin', '379.44', 'WATCHES', '25' ),
              ('Wrench set', '199.44', 'TOOLS', '25' )              
              ''')
    conn.commit()
    conn.close()
except sqlite3.OperationalError as e:
    print(e)
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
        