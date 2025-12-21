import sqlite3

# Connect to the database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Check the users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("Users table:")
for row in rows:
    print(row)

# Check the table schema
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("\nUsers table schema:")
for column in columns:
    print(column)

conn.close()