import sqlite3

def check_schema():
    conn = sqlite3.connect("data/mailforge.db")
    cursor = conn.cursor()
    
    print("--- campaigns table ---")
    cursor.execute("PRAGMA table_info(campaigns)")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- recipients table ---")
    cursor.execute("PRAGMA table_info(recipients)")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- events table ---")
    cursor.execute("PRAGMA table_info(events)")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    check_schema()
