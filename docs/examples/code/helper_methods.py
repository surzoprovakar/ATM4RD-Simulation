import sqlite3
import os

def db_generatoor():

    # Replica A
    connA = sqlite3.connect('Replica_A.db') 
    cA = connA.cursor()
    cA.execute('''
            CREATE TABLE IF NOT EXISTS sync_history
            ([requester] TEXT, [current_value] TEXT, 
            [req_value] TEXT, [type] TEXT, [req_trust] TEXT, 
            [updated_trust] TEXT, [req_time] TEXT, 
            [receive_time] TEXT, [decision] TEXT, [final_value] TEXT)
            ''')
    connA.commit()

    # Replica B
    connB = sqlite3.connect('Replica_B.db') 
    cB = connB.cursor()
    cB.execute('''
            CREATE TABLE IF NOT EXISTS sync_history
            ([requester] TEXT, [current_value] TEXT, 
            [req_value] TEXT, [type] TEXT, [req_trust] TEXT, 
            [updated_trust] TEXT, [req_time] TEXT, 
            [receive_time] TEXT, [decision] TEXT, [final_value] TEXT)
            ''')
    connB.commit()

    # Replica C
    connC = sqlite3.connect('Replica_C.db') 
    cC = connC.cursor()
    cC.execute('''
            CREATE TABLE IF NOT EXISTS sync_history
            ([requester] TEXT, [current_value] TEXT, 
            [req_value] TEXT, [type] TEXT, [req_trust] TEXT, 
            [updated_trust] TEXT, [req_time] TEXT, 
            [receive_time] TEXT, [decision] TEXT, [final_value] TEXT)
            ''')
    connC.commit()

    # Replica D
    connD = sqlite3.connect('Replica_D.db') 
    cD = connD.cursor()
    cD.execute('''
            CREATE TABLE IF NOT EXISTS sync_history
            ([requester] TEXT, [current_value] TEXT, 
            [req_value] TEXT, [type] TEXT, [req_trust] TEXT, 
            [updated_trust] TEXT, [req_time] TEXT, 
            [receive_time] TEXT, [decision] TEXT, [final_value] TEXT)
            ''')
    connD.commit()

    return cA, connA, cB, connB, cC, connC, cD, connD


def db_insert(c, conn, requester, current_value, req_value, type,
        req_trust, updated_trust, req_time, receive_time, decision, final_value):
    c.execute('''
          INSERT OR REPLACE INTO sync_history (requester, current_value,
          req_value, type, req_trust, updated_trust, req_time,
          receive_time, decision, final_value)

                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (requester, current_value, req_value, type, req_trust,
          updated_trust, req_time, receive_time, decision, final_value))

    conn.commit()


def file_generator():
    if os.path.exists('Replica A.txt') == False:
        fA = open("Replica A.txt", "a")
    else:
        os.remove('Replica A.txt')
        fA = open("Replica A.txt", "a")

    if os.path.exists('Replica B.txt') == False:
        fB = open("Replica B.txt", "a")
    else:
        os.remove('Replica B.txt')
        fB = open("Replica B.txt", "a")

    if os.path.exists('Replica C.txt') == False:
        fC = open("Replica C.txt", "a")
    else:
        os.remove('Replica C.txt')
        fC = open("Replica C.txt", "a")

    if os.path.exists('Replica D.txt') == False:
        fD = open("Replica D.txt", "a")
    else:
        os.remove('Replica D.txt')
        fD = open("Replica D.txt", "a")
    
    return fA, fB, fC, fD