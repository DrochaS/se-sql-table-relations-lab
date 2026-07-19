# SQL Joins Guide for Beginners

This guide is for someone new to SQL who wants to understand how to use joins to combine data from multiple tables.

## What is a join?
A join lets you combine rows from two or more tables based on a related column between them. Instead of keeping data isolated in separate tables, joins allow you to read it together in a single result.

## Why use joins?
- To answer questions that involve multiple tables
- To avoid duplicate data and keep the database normalized
- To connect related information like customers and orders, employees and offices, or products and sales

## Common join types

### 1. INNER JOIN
Returns only rows that have matching values in both tables.

Example: Get employees who work at an office.
```sql
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees AS e
JOIN offices AS o ON e.officeCode = o.officeCode;
```
This returns only employees whose `officeCode` exists in `offices`.

### 2. LEFT JOIN (LEFT OUTER JOIN)
Returns all rows from the left table, plus matching rows from the right table. If there is no match, the right table columns are `NULL`.

Example: Get all employees and their office location, even if an employee has no office assigned.
```sql
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees AS e
LEFT JOIN offices AS o ON e.officeCode = o.officeCode;
```
This will include every employee. If an employee does not have an office, `city` and `state` will be `NULL`.

### 3. RIGHT JOIN (RIGHT OUTER JOIN)
Returns all rows from the right table, plus matching rows from the left table. SQLite does not support `RIGHT JOIN`, but the concept is the same as `LEFT JOIN` with the table order swapped.

Example concept: Get all offices and any employees who work there.
```sql
SELECT e.firstName, e.lastName, o.city
FROM employees AS e
RIGHT JOIN offices AS o ON e.officeCode = o.officeCode;
```
In SQLite, you would instead write it as:
```sql
SELECT e.firstName, e.lastName, o.city
FROM offices AS o
LEFT JOIN employees AS e ON e.officeCode = o.officeCode;
```

### 4. FULL OUTER JOIN
Returns rows when there is a match in either table. SQLite does not support it directly, but the idea is to include rows that exist in one table or the other, or both.

### 5. CROSS JOIN
Returns every possible combination of rows from both tables. Use this rarely, only when you really need every pair of rows.

Example: Pair every employee with every office.
```sql
SELECT e.firstName, o.city
FROM employees AS e
CROSS JOIN offices AS o;
```

### 6. SELF JOIN
A table joined to itself. This is useful when rows in a table have relationships with other rows in the same table.

Example: Find each employee and their manager (when the manager is also an employee):
```sql
SELECT e.firstName AS employee, m.firstName AS manager
FROM employees AS e
LEFT JOIN employees AS m ON e.reportsTo = m.employeeNumber;
```

## Example use cases in a business database

### Find Boston employees
```sql
SELECT e.firstName, e.lastName, e.jobTitle
FROM employees AS e
JOIN offices AS o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
```

### Find offices with no employees
```sql
SELECT o.officeCode, o.city
FROM offices AS o
LEFT JOIN employees AS e ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0;
```

### Find customers who have never placed an order
```sql
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers AS c
LEFT JOIN orders AS o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL;
```

## How to read a join query
1. Start with the main table you want to query.
2. Decide which table contains the related data.
3. Use `ON` to specify how the tables are connected.
4. Choose the join type based on whether you need unmatched rows included.

## Tips for beginners
- Use aliases like `e` and `o` to make queries easier to read.
- Test your query with a simple `SELECT *` first.
- If results are missing, check whether the join should be `INNER` or `LEFT`.
- If you see duplicate rows, make sure the join conditions are correct.

## Summary
Joins are a powerful way to combine information from multiple tables. The most common joins are:
- `INNER JOIN`: only matching rows from both tables
- `LEFT JOIN`: all rows from the left table, and matching rows from the right
- `RIGHT JOIN`: all rows from the right table, and matching rows from the left
- `CROSS JOIN`: every combination of rows
- `SELF JOIN`: a table joined with itself

Once you understand these patterns, you can answer richer questions from your data.
