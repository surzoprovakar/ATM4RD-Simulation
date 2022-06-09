import sqlite3

def db_gen():
    conn = sqlite3.connect('test_database.db') 
    c = conn.cursor()
    
    c.execute('''
            CREATE TABLE IF NOT EXISTS products
            ([product_id] INTEGER, 
            [product_name] TEXT)
            ''')
            
    c.execute('''
            CREATE TABLE IF NOT EXISTS prices
            ([product_id] INTEGER, [price] INTEGER)
            ''')
    conn.commit()
    return c, conn
                        
cc = "Macbook"
table = "products"
c, conn = db_gen()
c.execute('''
          INSERT OR REPLACE INTO {} (product_id, product_name)

                VALUES
                (?, ?),
                (2,'Printer'),
                (3,'Tablet'),
                (4,'Desk'),
                (5,'Kettle')
          '''.format(table), (1, cc))

c.execute('''
          INSERT OR REPLACE INTO prices (product_id, price)

                VALUES
                (1,200),
                (2,200),
                (3,300),
                (4,450),
                (5,150),
                (1,400)
          ''')

conn.commit()
conn.close()