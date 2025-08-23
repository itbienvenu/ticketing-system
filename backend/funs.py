import sqlite3
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

data = "UserID:12345;Role:Admin"
encrypted = cipher.encrypt(data.encode())
decrypted = cipher.decrypt(encrypted).decode()
# print(encrypted, decrypted)

# print(key, cipher)

def change_something():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    # cursor.execute("""CREATE TABLE buses_new (
    # id TEXT PRIMARY KEY,
    # plate_number TEXT UNIQUE NOT NULL,
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    # -- exclude route_id
    # );
    #     """)
    # f = cursor.execute("""DROP TABLE buses""")
    # if f:
    #     print("Deleted")
    # cursor.execute("""ALTER TABLE bus_routes ADD COLUMN id TEXT PRIMARY KEY ;
    #   """)

    # cursor.execute("")
    # cursor.execute("""ALTER TABLE tickets ADD COLUMN status ENUM('active', 'cancelled', 'deleted') DEFAULT 'active';""")
    # cursor.execute("PRAGMA foreign_keys=ON;")
#     cursor.execute("""
#     ALTER TABLE tickets 
#     ADD COLUMN mode TEXT CHECK(mode IN ('active', 'cancelled', 'deleted')) DEFAULT 'active';
# """)
    # conn.commit()

    conn.close()

# change_something()
