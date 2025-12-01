-- Retail Sales Analysis Queries

-- 1. Top-selling product by month
-- as SQLite's strftime returns string, so we group by that.
SELECT 
    strftime('%Y-%m', OrderDate) AS Month,
    p.ProductName,
    SUM(od.Quantity) AS TotalQuantity
FROM OrderDetails od
JOIN Orders o ON od.OrderID = o.OrderID
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY Month, p.ProductID
ORDER BY Month DESC, TotalQuantity DESC;

-- 2. Sales by region using JOIN + GROUP BY
SELECT 
    c.Region,
    SUM(o.TotalAmount) AS TotalSales
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY TotalSales DESC;

-- 3. Customers with total spend > threshold (using subqueries)
-- Threshold set to 1000 for demonstration
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Region,
    (SELECT SUM(TotalAmount) FROM Orders WHERE CustomerID = c.CustomerID) as TotalSpend
FROM Customers c
WHERE c.CustomerID IN (
    SELECT CustomerID 
    FROM Orders 
    GROUP BY CustomerID 
    HAVING SUM(TotalAmount) > 1000
)
ORDER BY TotalSpend DESC;
