import sqlite3

def change_something():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    # cursor.execute("""ALTER TABLE routes ADD COLUMN created_at""")
    # cursor.execute("""ALTER TABLE routes ADD COLUMN updated_at""")
    cursor.close()