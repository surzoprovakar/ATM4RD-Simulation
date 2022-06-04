import sqlite3
import os


def SLA(trust, delta):
    decision = ""
    updated_trust = 0.0
    if trust >= 0.9:
        # Very Trusty
        if delta <= 20: # and time_freq <= 20:
            decision = "Accepted"
            # Max trust value is 1.0
            if trust < 1.0:
                updated_trust = trust + 0.1
                if updated_trust > 1:
                    updated_trust = 1.0
            else:
                updated_trust = trust 
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.6 and trust < 0.9:
        # Medium Trusty
        if delta <= 15: # and time_freq <= 18:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.5 and trust < 0.6:
        # Low Trusty
        if delta <= 10: # and time_freq <= 12:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust < 0.5 and trust >= 0.25:
        # Less Untrustworthy
        if delta <= 7: # and time_freq <= 0.8:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    else:
        # Very Untrustworthy
        if delta <= 3: # and time_freq <= 5:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            if trust > 0.0:
                # Min trust value is 0.0
                updated_trust = trust - 0.1
                if updated_trust < 0.0:
                    updated_trust = 0
            else:
                updated_trust = trust
    
    return decision, updated_trust


def db_generatoor():

    # Replica A
    connA = sqlite3.connect('Replica_A.db') 
    cA = connA.cursor()
    cA.execute('''
            CREATE TABLE IF NOT EXISTS sync_history
            ([requester] TEXT, [current_value] TEXT, 
            [req_value] TEXT, [delta] TEXT, [req_trust] TEXT, 
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
            [req_value] TEXT, [delta] TEXT, [req_trust] TEXT, 
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
            [req_value] TEXT, [delta] TEXT, [req_trust] TEXT, 
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
            [req_value] TEXT, [delta] TEXT, [req_trust] TEXT, 
            [updated_trust] TEXT, [req_time] TEXT, 
            [receive_time] TEXT, [decision] TEXT, [final_value] TEXT)
            ''')
    connD.commit()

    return cA, connA, cB, connB, cC, connC, cD, connD


def db_insert(c, conn, requester, current_value, req_value, delta,
        req_trust, updated_trust, req_time, receive_time, decision, final_value):
    c.execute('''
          INSERT OR REPLACE INTO sync_history (requester, current_value,
          req_value, delta, req_trust, updated_trust, req_time,
          receive_time, decision, final_value)

                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (requester, current_value, req_value, delta, req_trust,
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