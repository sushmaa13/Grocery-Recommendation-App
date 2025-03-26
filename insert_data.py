import sqlite3
from datetime import datetime

def insert_sample_data(db_name="grocery.db"):
    # Connect to your existing database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get the current month in YYYY-MM format
    current_month = datetime.now().strftime("%Y-%m")
    
    # Prepare sample data.
    # Note: For the new detailed columns, we are setting default values (None or 0)
    # You can adjust these values as needed.
    sample_data = [
    ("Milk", 166.0, 2, "2025-04-01", "Yes", 0, 0, 0, current_month),
    ("Eggs", 996.0, 12, "2025-04-15", "Yes", 0, 0, 0, current_month),
    ("Bread", 83.0, 1, "2025-03-20", "Yes", 0, 0, 0, current_month),
    ("Rice", 415.0, 5, "2025-05-10", "Yes", 0, 0, 0, current_month),
    ("Oil", 500.0, 2, "2025-06-01", "Yes", 0, 0, 0, current_month)
]
    
    # Insert sample data into grocery_items table.
    # The columns are: name, cost_inr, quantity, expiry_date, completely_used, used_quantity, donated_quantity, expired_quantity, month
    cursor.executemany("""
        INSERT INTO grocery_items (name, cost_inr, quantity, expiry_date, completely_used, used_quantity, donated_quantity, expired_quantity, month)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_data)
    
    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
