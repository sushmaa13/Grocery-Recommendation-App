import sqlite3
import pandas as pd
from datetime import datetime

def fetch_current_month_data(db_name="grocery.db"):
    """
    Connects to the SQLite database and fetches data for the current month.
    """
    conn = sqlite3.connect(db_name)
    # Format the current month as YYYY-MM (e.g., "2025-03")
    current_month = datetime.now().strftime("%Y-%m")
    query = "SELECT * FROM grocery_items WHERE month = ?"
    df = pd.read_sql_query(query, conn, params=(current_month,))
    conn.close()
    return df

def generate_next_month_recommendations(df):
    """
    Generates recommendations for next month's grocery quantities based on user feedback.
    
    Rules:
      - "Used": Increase the quantity by 10% (with rounding).
      - "Donated": Decrease the quantity to 50% (ensure at least 1).
      - "Expired": Keep the same quantity (but flag for review if needed).
    """
    recommendations = []
    for _, row in df.iterrows():
        qty = row["quantity"]
        status = row["feedback"]
        
        if status == "Used":
            recommended_qty = int(qty * 1.1 + 0.5)  # Add a 10% buffer
        elif status == "Donated":
            recommended_qty = max(int(qty * 0.5), 1)  # Reduce by half but order at least 1
        elif status == "Expired":
            recommended_qty = qty  # Reorder same amount
        else:
            # If feedback hasn't been provided, you can either skip or use the same quantity.
            recommended_qty = qty
        recommendations.append(recommended_qty)
    
    df["next_month_quantity"] = recommendations
    return df

def main():
    # Fetch current month's data from the database
    df = fetch_current_month_data()
    print("Current Month Data:")
    print(df)
    
    # Generate recommendations for next month
    df_recommend = generate_next_month_recommendations(df)
    print("\nRecommendations for Next Month:")
    print(df_recommend[["name", "quantity", "feedback", "next_month_quantity"]])

if __name__ == "__main__":
    main()
