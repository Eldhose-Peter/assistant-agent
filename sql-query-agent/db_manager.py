import sqlite3
import os
import json
import sys

db_path = 'data_set/sales_order.sqlite'
query_file = 'data_set/previous_queries.json'

def read_previous_queries():
    """
    Read a JSON file containing queries and convert to the specified text format.
        
    Returns:
        str: Formatted text output
    """
    try:
        # Read the JSON file
        with open(query_file, 'r') as file:
            data = json.load(file)
        
        # Check if the file has the expected structure
        if 'queries' not in data:
            print("Error: The JSON file doesn't have a 'queries' key.")
            return None
        
        # Process each query
        formatted_output = ""
        for query in data['queries']:
            if 'user_input' in query and 'sql_query' in query:
                formatted_output += f"User input: {query['user_input']}\n\n"
                formatted_output += f"SQL query: {query['sql_query']}\n\n"
                formatted_output += "-" * 50 + "\n\n"
        
        return formatted_output
        
    except FileNotFoundError:
        print(f"Error: File '{query_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: '{query_file}' is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def read_db_schema():
    """
    Read the schema of a SQLite database and return it in a specific formatted string.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        str: A formatted string containing the schema information
    """
    if not os.path.exists(db_path):
        return f"Error: Database file '{db_path}' not found."

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            conn.close()
            return "No tables found in the database."
            
        result = []
        
        # For each table, get detailed schema information
        table_count = 0
        for table in tables:
            table_name = table[0]
            
            # Skip SQLite internal tables
            if table_name.startswith("sqlite_"):
                continue
                
            table_count += 1
            
            # Get table info (columns, types, etc.)
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            # Format the columns as requested
            columns_str = ", ".join([f"{col[1]} {col[2]}" for col in columns_info])
            
            # Format the entire table line
            table_line = f"{table_count} - {table_name} ({columns_str})"
            
            result.append(table_line)
        
        # Close the connection
        conn.close()
        
        # Join all table lines with newlines
        return "\n\n".join(result)
        
    except sqlite3.Error as e:
        return f"SQLite error: {e}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print("Task Manager initialized.")