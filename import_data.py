import pandas as pd
import sqlite3
import random
import os

csv_file = 'dataset/Amazon Sale Report.csv'
db_file = 'retail_sales.db'
schema_file = 'schema.sql'

def setup_database():
    if os.path.exists(db_file):
        os.remove(db_file)
    
    conn = sqlite3.connect(db_file)
    with open(schema_file, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("Database initialized.")

def import_data():
    print("Reading CSV...")
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0).astype(int)
    
    
    df = df.dropna(subset=['Order ID', 'SKU'])

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("Processing Customers...")
 
    unique_orders = df['Order ID'].unique()
    num_customers = max(1, len(unique_orders) // 3)
    
    customers = []
    for i in range(1, num_customers + 1):
        customers.append((i, f"Customer_{i}", random.choice(['North', 'South', 'East', 'West']), f"user{i}@example.com"))
    
    cursor.executemany("INSERT INTO Customers (CustomerID, CustomerName, Region, Contact) VALUES (?, ?, ?, ?)", customers)
    
    
    order_to_customer = {order_id: random.randint(1, num_customers) for order_id in unique_orders}

    print("Processing Products...")
    
    products = df[['SKU', 'Style', 'Category', 'Amount']].drop_duplicates(subset=['SKU'])
    
    product_data = []
    for _, row in products.iterrows():
        
        product_data.append((row['SKU'], row['Style'], row['Category'], row['Amount']))
    
    cursor.executemany("INSERT OR IGNORE INTO Products (ProductID, ProductName, Category, Price) VALUES (?, ?, ?, ?)", product_data)

    print("Processing Orders and Details...")
    
    
    
    orders_data = []
    order_details_data = []
    
    
    
    grouped = df.groupby('Order ID')
    
    for order_id, group in grouped:
        customer_id = order_to_customer[order_id]
        order_date = group.iloc[0]['Date']
        
        
        ship_state = group.iloc[0]['ship-state']
        if pd.isna(ship_state):
            ship_state = "Unknown"
            
        cursor.execute("UPDATE Customers SET Region = ? WHERE CustomerID = ?", (ship_state, customer_id))
        
        total_amount = group['Amount'].sum()
        
        orders_data.append((order_id, customer_id, order_date, total_amount))
        
        for _, row in group.iterrows():
            order_details_data.append((order_id, row['SKU'], row['Qty'], row['Amount']))

    cursor.executemany("INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES (?, ?, ?, ?)", orders_data)
    cursor.executemany("INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)", order_details_data)

    conn.commit()
    conn.close()
    print("Data import complete.")

if __name__ == "__main__":
    setup_database()
    import_data()
