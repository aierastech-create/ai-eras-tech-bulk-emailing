import sqlite3

def check_query():
    conn = sqlite3.connect("data/mailforge.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    campaign_id = 1 # Assuming there's at least one campaign or we just check the query structure
    
    try:
        query = """
            SELECT r.subject_used, 
                   COUNT(r.id) as sent,
                   COUNT(DISTINCT e.id) as opens
            FROM recipients r
            LEFT JOIN events e ON r.id = e.recipient_id AND e.event_type = 'open'
            WHERE r.campaign_id = ?
            GROUP BY r.subject_used
        """
        cursor.execute(query, (campaign_id,))
        print("Query executed successfully")
    except Exception as e:
        print(f"Query failed: {e}")
        
    conn.close()

if __name__ == "__main__":
    check_query()
