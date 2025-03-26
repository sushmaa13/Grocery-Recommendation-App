from flask import Flask, render_template, request, redirect, url_for 
import sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
DATABASE = "grocery.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM grocery_items WHERE month = strftime('%Y-%m', 'now')").fetchall()
    conn.close()
    return render_template("index.html", items=items)

# Updated /update route to process detailed feedback
@app.route("/update", methods=["POST"])
def update_feedback():
    conn = get_db_connection()
    current_month = datetime.now().strftime("%Y-%m")
    # Get all items for the current month
    items = conn.execute("SELECT * FROM grocery_items WHERE month = ?", (current_month,)).fetchall()
    
    for item in items:
        item_id = item["id"]
        # Retrieve the radio button value for "completely_used"
        completely_used = request.form.get(f"completely_used_{item_id}", "Yes")
        if completely_used == "Yes":
            # If completely used, assume full quantity was used.
            used_quantity = item["quantity"]
            donated_quantity = 0
            expired_quantity = 0
        else:
            # Retrieve the detailed feedback values.
            used_quantity = int(request.form.get(f"used_{item_id}", 0))
            donated_quantity = int(request.form.get(f"donated_{item_id}", 0))
            expired_quantity = int(request.form.get(f"expired_{item_id}", 0))
        
        # Update the database with the detailed feedback
        conn.execute("""
            UPDATE grocery_items 
            SET completely_used = ?, used_quantity = ?, donated_quantity = ?, expired_quantity = ?
            WHERE id = ?
        """, (completely_used, used_quantity, donated_quantity, expired_quantity, item_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Updated recommendation function to calculate recommended quantity, estimated cost, and amount saved
def generate_next_month_recommendations(df):
    recommendations = []
    total_estimated_cost = 0
    total_amount_saved = 0
    
    for _, row in df.iterrows():
        original_qty = row["quantity"]
        cost_inr = row["cost_inr"]
        cost_per_unit = cost_inr / original_qty
        
        # Treat missing completely_used as "Yes"
        if row.get("completely_used", "Yes") == "Yes":
            used_qty = original_qty
            recommended_qty = int(original_qty * 1.1 + 0.5)  # Add 10% buffer
        else:
            used_qty = row.get("used_quantity", 0)
            recommended_qty = int(used_qty * 1.1 + 0.5)
        
        estimated_cost = recommended_qty * cost_per_unit
        amount_saved = (original_qty - used_qty) * cost_per_unit
        
        recommendations.append({
            "name": row["name"],
            "original_quantity": original_qty,
            "used_quantity": used_qty,
            "recommended_quantity": recommended_qty,
            "cost_inr": cost_inr,
            "estimated_cost": round(estimated_cost, 2),
            "amount_saved": round(amount_saved, 2)
        })
        total_estimated_cost += estimated_cost
        total_amount_saved += amount_saved
    
    # Return a DataFrame and the totals
    return pd.DataFrame(recommendations), round(total_estimated_cost, 2), round(total_amount_saved, 2)

@app.route("/recommendations")
def recommendations():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM grocery_items WHERE month = strftime('%Y-%m', 'now')", conn)
    conn.close()

    rec_df, total_estimated_cost, total_amount_saved = generate_next_month_recommendations(df)
    recommendations_list = rec_df.to_dict(orient="records")
    return render_template("recommendations.html", recommendations=recommendations_list, 
                           total_estimated_cost=total_estimated_cost, total_amount_saved=total_amount_saved)

if __name__ == "__main__":
    app.run(debug=True)
