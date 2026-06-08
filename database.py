import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect('chatbot.db')

# CREATE CURSOR
cursor = conn.cursor()

# CREATE TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# SAVE CHANGES
conn.commit()

# CLOSE CONNECTION
conn.close()

print("Database created successfully.")