import sqlite3
import uuid

# Connect to the SQLite database
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# wsgi.py
# from fastapi.middleware.wsgi import WSGIMiddleware
# from main import app as fastapi_app

# application = WSGIMiddleware(fastapi_app)


# Create the permissions table if it doesn't exist
# List of permissions to create
permissions = [
    "get_permission",
 
]


# Insert permissions
# for perm in permissions:
#     cursor.execute(
#         "INSERT OR IGNORE INTO permissions (id, name) VALUES (?, ?)",
#         (str(uuid.uuid4()), perm)
#     )

# cursor.execute("INSERT INTO roles (id, name) VALUES (?,?)", (str(uuid.uuid4()), "admin"))
cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?,?)", ("bf26aad1-17ac-4070-bdb2-8ee2f563a01d", "64c67587-db9d-411b-93ce-84ca6e4b72f7"))
# cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?,?)", ("f05ee908-62c8-4810-bc86-4721dc3aed3f", "4a19375c-b6a5-4025-8150-7ac7f4abf8b4"))
# cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?,?)", ("bf26aad1-17ac-4070-bdb2-8ee2f563a01d", "91c05ac9-128d-4b34-ae87-53195993779f"))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Permissions successfully created in tickets.db ✅")

