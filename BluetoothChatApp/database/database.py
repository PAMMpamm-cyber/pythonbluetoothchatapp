import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect("database/chat_app.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_pic TEXT
        )
    ''')

    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

def register_user(username, password):
    conn = sqlite3.connect("database/chat_app.db")
    cursor = conn.cursor()

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already taken!")
    
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("database/chat_app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

    conn.close()
