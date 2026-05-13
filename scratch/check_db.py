import sqlite3
db_path = "data/mailforge.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(campaigns)")
columns = cursor.fetchall()
print("Campaigns columns:")
for col in columns:
    print(col)

cursor.execute("SELECT * FROM campaigns LIMIT 1")
try:
    row = cursor.fetchone()
    print("Latest campaign:", dict(row) if row else "None")
except Exception as e:
    print("Error fetching row:", e)

conn.close()
