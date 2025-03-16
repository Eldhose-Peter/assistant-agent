Convert NLP to SQL queries

## Run

### Install Dependencies
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Intialise DB
Run `initialise_db.py`
Result `.sqlite` file created


## Sample interaction
```
Welcome to the AI Assistant. Type 'exit' to quit.
You: How many employees work in customer service department ?
Agent response: SELECT COUNT(*) FROM Employee WHERE Position LIKE '%customer%';
Query response: [(1,)]
You: List all products currently not in stock
Agent response: SELECT * FROM Product WHERE StockQuantity = 0;
Query response: []
You: List all products currently in stock
Agent response: SELECT * FROM Product WHERE StockQuantity > 0;
Query response: [(1, 'Laptop Pro X', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, 25, 5, 0), (2, 'Smartphone Y', 'Latest smartphone with 128GB storage and dual camera', 799.99, 50, 10, 0), (3, 'Wireless Headphones', 'Noise-cancelling wireless headphones with 30-hour battery life', 199.99, 100, 15, 0), (4, 'Smart Watch', 'Fitness tracker and smartwatch with heart rate monitor', 249.99, 30, 8, 0), (5, 'Tablet Z', '10-inch tablet with 64GB storage and stylus support', 349.99, 20, 5, 0), (6, 'Desk Chair', 'Ergonomic office chair with lumbar support', 149.99, 15, 3, 0), (7, 'Coffee Maker', 'Programmable coffee maker with thermal carafe', 79.99, 40, 10, 0), (8, 'Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 59.99, 75, 15, 0), (9, 'External Hard Drive', '2TB portable external hard drive', 89.99, 35, 7, 0), (10, 'Gaming Mouse', 'High-precision gaming mouse with customizable buttons', 49.99, 60, 12, 1)]
```


## Algorithm
1. NLP Analysis
3. SQL mapping
4. Query generation
5. Database Execution
6. Result Retrieval

## LLM Context
1. **Schema only**. We put the schema (using DDL) in the context window.
2. **Static examples**. We put static example SQL queries in the context windows.

## Scope for Improvement
#### Using contextually relevant examples

Enterprise data warehouses often contain 100s (or even 1000s) of tables, and an order of magnitude more queries that cover all the use cases within their organizations. Given the limited size of the context windows of modern LLMs, we can’t just shove all the prior queries and schema definitions into the prompt.

Soln:  more sophisticated ML approach - load embeddings of prior queries and the table schemas into a vector database, and only choose the most relevant queries / tables to the question asked. 

