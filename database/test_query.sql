--Test Queries for the database; The python program provides a command to automatically run and print the output of these queries.

--Test 1: Select all Employees who've been assigned to perform a Quality Test, and how many tests they've been assigned:
SELECT e.employee_ID, CONCAT(e.first_name, ' ', e.last_name) AS name, COUNT(q.test_ID) as tests_assigned
FROM Employee e INNER JOIN Quality_Test q ON e.employee_ID = q.performed_by
GROUP BY e.employee_ID, name
HAVING tests_assigned >= 1;

--Test 2: Select all Products (IDs and names) and the total quantity ordered for each (assumes the unit is the same for each product appearing multiple times)
SELECT p.product_ID, p.name, SUM(ol.quantity) as total_quantity
FROM Product p INNER JOIN Order_Line ol ON p.product_ID = ol.product_ID
GROUP BY p.product_ID, p.name

--Test 3: Print all Raw Materials (their ID, name, and default unit) and their total quantity used among Batch Consumptions
SELECT m.material_ID, m.name, m.default_unit, SUM(bc.quantity_used) as total_quantity_used
FROM Raw_Material m INNER JOIN Batch_Consumption bc ON m.material_ID = bc.material_ID
GROUP BY m.material_ID

--Test 4: Select all Plants and their total production capacity from completed batches
SELECT p.plant_ID, p.name, p.location, SUM(b.actual_quantity) as total_production
FROM Plant p 
INNER JOIN Unit u ON p.plant_ID = u.plant_ID
INNER JOIN Batch b ON u.unit_ID = b.unit_ID
WHERE b.status = 'Completed' AND b.actual_quantity IS NOT NULL
GROUP BY p.plant_ID, p.name, p.location;

--Test 5: Select all Customers and their total number of orders with total order value
SELECT c.customer_ID, c.name, c.industry, 
       COUNT(DISTINCT so.order_ID) as total_orders,
       SUM(ol.quantity * ol.unit_price) as total_order_value
FROM Customer c 
INNER JOIN Sales_Order so ON c.customer_ID = so.customer_ID
INNER JOIN Order_Line ol ON so.order_ID = ol.order_ID
GROUP BY c.customer_ID, c.name, c.industry;
