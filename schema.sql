-- Retail Sales Database Schema

-- Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY,
    CustomerName TEXT NOT NULL,
    Region TEXT,
    Contact TEXT -- Placeholder for contact info
);

-- Products Table
CREATE TABLE IF NOT EXISTS Products (
    ProductID TEXT PRIMARY KEY, -- Using SKU as ProductID
    ProductName TEXT, -- Category + Style as name since real name is missing
    Category TEXT,
    Price REAL
);

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders (
    OrderID TEXT PRIMARY KEY,
    CustomerID INTEGER,
    OrderDate DATE,
    TotalAmount REAL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- OrderDetails Table
CREATE TABLE IF NOT EXISTS OrderDetails (
    OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID TEXT,
    ProductID TEXT,
    Quantity INTEGER,
    UnitPrice REAL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
