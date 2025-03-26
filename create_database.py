import sqlite3

def create_database(db_name="grocery.db"):
    # Connect to the database (if it doesn't exist, it will be created)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # SQL command to create a table for your grocery items with detailed feedback columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grocery_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost_inr REAL NOT NULL,
        quantity INTEGER NOT NULL,
        expiry_date TEXT,
        completely_used TEXT,          -- New column: "Yes" or "No"
        used_quantity INTEGER DEFAULT 0, -- New column: number of units used
        donated_quantity INTEGER DEFAULT 0, -- New column: number of units donated
        expired_quantity INTEGER DEFAULT 0, -- New column: number of units expired
        month TEXT
    );
    """)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
