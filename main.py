# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees AS e
    JOIN offices AS o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices AS o
    LEFT JOIN employees AS e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees AS e
    LEFT JOIN offices AS o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers AS c
    LEFT JOIN orders AS o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
    FROM payments AS p
    JOIN customers AS c ON p.customerNumber = c.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
    FROM employees AS e
    JOIN customers AS c ON c.salesRepEmployeeNumber = e.employeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
    ORDER BY numcustomers DESC
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM orderdetails AS od
    JOIN products AS p ON od.productCode = p.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM orderdetails AS od
    JOIN orders AS o ON od.orderNumber = o.orderNumber
    JOIN products AS p ON od.productCode = p.productCode
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices AS o
    JOIN employees AS e ON o.officeCode = e.officeCode
    JOIN customers AS c ON c.salesRepEmployeeNumber = e.employeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
    WITH low_products AS (
        SELECT od.productCode
        FROM orderdetails AS od
        JOIN orders AS o ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, off.city, e.officeCode
    FROM employees AS e
    JOIN customers AS c ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN orders AS o ON o.customerNumber = c.customerNumber
    JOIN orderdetails AS od ON od.orderNumber = o.orderNumber
    JOIN low_products AS lp ON od.productCode = lp.productCode
    JOIN offices AS off ON e.officeCode = off.officeCode
    ORDER BY e.lastName, e.firstName
""", conn)

conn.close()