import sqlite3
import os

def print_table(cursor, table_name):
    """Print all data from a specified table"""
    print(f"\n===== {table_name} TABLE =====")
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    print(" | ".join(columns))
    print("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
    
    # Get and print data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if not rows:
        print("No data found")
        return
    
    for row in rows:
        print(" | ".join(str(item) for item in row))
    
    print(f"Total rows: {len(rows)}")

def main():
    db_name = 'sales_order.sqlite'
    
    # Check if the database file exists
    if not os.path.exists(db_name):
        print(f"Error: Database file '{db_name}' not found.")
        print("Please run the create-sales-db.py script first to create the database.")
        return
    
    # Connect to the database
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"Database '{db_name}' contains {len(tables)} tables: {', '.join(tables)}")
        
        # Print data from each table
        for table in tables:
            print_table(cursor, table)
        
        # Print some summary statistics
        print("\n===== SUMMARY STATISTICS =====")
        
        # Total number of customers
        cursor.execute("SELECT COUNT(*) FROM Customer")
        print(f"Total customers: {cursor.fetchone()[0]}")
        
        # Total number of products
        cursor.execute("SELECT COUNT(*) FROM Product")
        print(f"Total products: {cursor.fetchone()[0]}")
        
        # Total number of orders
        cursor.execute("SELECT COUNT(*) FROM SalesOrder")
        print(f"Total orders: {cursor.fetchone()[0]}")
        
        # Average order value
        cursor.execute("""
            SELECT AVG(total) FROM (
                SELECT SalesOrderID, SUM(TotalPrice) as total 
                FROM LineItem 
                GROUP BY SalesOrderID
            )
        """)
        avg_order = cursor.fetchone()[0]
        print(f"Average order value: ${avg_order:.2f}")
        
        # Top selling product
        cursor.execute("""
            SELECT p.ProductName, SUM(li.Quantity) as total_sold
            FROM LineItem li
            JOIN Product p ON li.ProductID = p.ProductID
            GROUP BY li.ProductID
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        top_product = cursor.fetchone()
        print(f"Top selling product: {top_product[0]} (Qty: {top_product[1]})")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()