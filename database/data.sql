-- 1. Plant (no foreign keys)
INSERT INTO Plant (name, location, start_date, total_capacity_tons) VALUES
('BASF Ludwigshafen', 'Ludwigshafen, Germany', '1865-04-06', 250000.00),
('BASF Geismar', 'Geismar, Louisiana, USA', '1958-03-15', 180000.00),
('BASF Antwerp', 'Antwerp, Belgium', '1964-07-20', 150000.00),
('BASF Shanghai', 'Shanghai, China', '2005-11-10', 120000.00),
('BASF Freeport', 'Freeport, Texas, USA', '1958-09-01', 200000.00);

-- 2. Unit (foreign key to Plant)
INSERT INTO Unit (name, unit_type, status, plant_ID) VALUES
('Ammonia Synthesis A1', 'Reactor', 'Active', 1),
('Ammonia Synthesis A2', 'Reactor', 'Active', 1),
('Ethylene Cracker E1', 'Cracker', 'Active', 2),
('Polymerization P1', 'Reactor', 'Active', 2),
('Distillation D1', 'Separator', 'Maintenance', 3),
('Hydrogenation H1', 'Reactor', 'Active', 3),
('Oxidation O1', 'Reactor', 'Active', 4),
('Crystallization C1', 'Crystallizer', 'Active', 4),
('Neutralization N1', 'Reactor', 'Active', 5),
('Compression Unit C2', 'Compressor', 'Inactive', 5);

-- 3. Raw_Material (foreign key to Unit)
INSERT INTO Raw_Material (name, hazard_class, physical_state, default_unit, unit_ID) VALUES
('Ammonia', 'Class 2.3 - Toxic Gas', 'Gas', 'kg', 1),
('Ethylene', 'Class 2.1 - Flammable Gas', 'Gas', 'kg', 3),
('Propylene', 'Class 2.1 - Flammable Gas', 'Gas', 'kg', 4),
('Hydrogen', 'Class 2.1 - Flammable Gas', 'Gas', 'm3', 6),
('Sulfuric Acid', 'Class 8 - Corrosive', 'Liquid', 'L', 9),
('Methanol', 'Class 3 - Flammable Liquid', 'Liquid', 'L', 7),
('Catalyst Powder', NULL, 'Solid', 'kg', 8),
('Nitrogen', NULL, 'Gas', 'm3', 2);

-- 4. Supplier (foreign key to Raw_Material)
INSERT INTO Supplier (name, contact_name, phone, email, address, material_ID) VALUES
('Yara International', 'Hans Mueller', '+49-621-6000', 'hans.mueller@yara.com', 'Oslo, Norway', 1),
('Shell Chemical', 'Sarah Johnson', '+1-713-241-6161', 'sarah.johnson@shell.com', 'Houston, TX, USA', 2),
('LyondellBasell', 'Michael Chen', '+1-713-309-7200', 'michael.chen@lyondellbasell.com', 'Houston, TX, USA', 3),
('ExxonMobil Chemical', 'David Williams', '+1-832-624-6000', 'david.williams@exxon.com', 'Spring, TX, USA', 4),
('Air Liquide', 'Marie Dubois', '+33-1-4062-5555', 'marie.dubois@airliquide.com', 'Paris, France', 8),
('INEOS Enterprises', 'James Brown', '+41-21-627-7111', 'james.brown@ineos.com', 'Rolle, Switzerland', 4),
('Methanex', 'Robert Taylor', '+1-604-661-2600', 'robert.taylor@methanex.com', 'Vancouver, BC, Canada', 7),
('Kemira', 'Anna Schmidt', '+358-10-8611', 'anna.schmidt@kemira.com', 'Helsinki, Finland', 6);

-- 5. Employee (foreign key to Plant)
INSERT INTO Employee (first_name, last_name, role, department, email, hire_date, plant_ID) VALUES
('Klaus', 'Schmidt', 'Plant Manager', 'Operations', 'klaus.schmidt@basf.com', '2010-03-15', 1),
('Maria', 'Fischer', 'Production Supervisor', 'Operations', 'maria.fischer@basf.com', '2015-06-20', 1),
('John', 'Anderson', 'Lead Operator', 'Production', 'john.anderson@basf.com', '2012-08-10', 2),
('Emily', 'Davis', 'Quality Control Specialist', 'Quality', 'emily.davis@basf.com', '2016-02-28', 2),
('Pierre', 'Laurent', 'Process Engineer', 'Engineering', 'pierre.laurent@basf.com', '2014-11-05', 3),
('Sophie', 'Martin', 'Lead Operator', 'Production', 'sophie.martin@basf.com', '2013-04-12', 3),
('Wei', 'Zhang', 'Production Supervisor', 'Operations', 'wei.zhang@basf.com', '2017-09-01', 4),
('Li', 'Wang', 'Quality Manager', 'Quality', 'li.wang@basf.com', '2016-07-15', 4),
('Carlos', 'Rodriguez', 'Lead Operator', 'Production', 'carlos.rodriguez@basf.com', '2011-05-20', 5),
('Jennifer', 'Wilson', 'Lab Technician', 'Quality', 'jennifer.wilson@basf.com', '2018-01-10', 5),
('Hans', 'Becker', 'Process Operator', 'Production', 'hans.becker@basf.com', '2019-03-22', 1),
('Anna', 'Kowalski', 'Quality Analyst', 'Quality', 'anna.kowalski@basf.com', '2020-06-15', 3);

-- 6. Product (no foreign keys)
INSERT INTO Product (name, grade, physical_state, hazard_class, sds_code) VALUES
('Polyethylene', 'LDPE-1840', 'Solid', 'Non-hazardous', 'SDS-PE-001'),
('Polypropylene', 'PP-H301', 'Solid', 'Non-hazardous', 'SDS-PP-002'),
('Ammonia Solution', '25% Technical', 'Liquid', 'Class 8 - Corrosive', 'SDS-NH3-003'),
('Styrene Monomer', 'Polymer Grade', 'Liquid', 'Class 3 - Flammable', 'SDS-STY-004'),
('Butanol', 'Industrial Grade', 'Liquid', 'Class 3 - Flammable', 'SDS-BUT-005'),
('Acrylic Acid', '99.5% Pure', 'Liquid', 'Class 8 - Corrosive', 'SDS-AA-006'),
('Polyamide 6', 'PA6-B27', 'Solid', 'Non-hazardous', 'SDS-PA6-007'),
('Methyl Methacrylate', 'MMA-100', 'Liquid', 'Class 3 - Flammable', 'SDS-MMA-008');

-- 7. Batch (foreign keys to Unit, Product, Employee)
INSERT INTO Batch (start_time, end_time, target_quantity, actual_quantity, status, unit_ID, product_ID, lead_op_ID) VALUES
('2024-11-01 08:00:00', '2024-11-01 16:30:00', 5000.00, 4985.50, 'Completed', 1, 3, 2),
('2024-11-02 09:00:00', '2024-11-03 14:00:00', 12000.00, 11950.00, 'Completed', 3, 1, 3),
('2024-11-05 07:30:00', '2024-11-06 18:00:00', 8000.00, 7920.00, 'Completed', 4, 2, 3),
('2024-11-10 10:00:00', '2024-11-11 22:00:00', 6000.00, 5980.00, 'Completed', 6, 4, 6),
('2024-11-15 06:00:00', NULL, 10000.00, NULL, 'In Progress', 7, 5, 9),
('2024-11-20 08:00:00', NULL, 7500.00, NULL, 'Planned', 8, 7, 9),
('2024-11-12 14:00:00', '2024-11-13 20:00:00', 4500.00, 4475.00, 'Completed', 9, 6, 9),
('2024-11-08 11:00:00', NULL, 9000.00, NULL, 'Cancelled', 4, 2, 3);

-- 8. Batch_Consumption (foreign keys to Batch, Raw_Material)
INSERT INTO Batch_Consumption (quantity_used, unit, batch_ID, material_ID) VALUES
(1200.00, 'kg', 1, 1),
(8500.00, 'kg', 2, 2),
(5800.00, 'kg', 3, 3),
(3200.00, 'm3', 4, 4),
(580.00, 'L', 4, 5),
(2400.00, 'L', 7, 6),
(650.00, 'kg', 7, 7);

-- 9. Quality_Test (foreign keys to Batch, Employee)
INSERT INTO Quality_Test (sample_time, result_status, comments, batch_ID, performed_by) VALUES
('2024-11-01 12:00:00', 'Pass', 'All parameters within specification. pH 8.2, purity 99.1%', 1, 4),
('2024-11-01 16:00:00', 'Pass', 'Final product meets quality standards', 1, 4),
('2024-11-02 18:00:00', 'Pass', 'Density and melt flow index acceptable', 2, 4),
('2024-11-03 10:00:00', 'Pass', 'Molecular weight distribution confirmed', 2, 4),
('2024-11-05 14:00:00', 'Fail', 'Viscosity slightly below specification. Batch adjusted.', 3, 10),
('2024-11-06 16:00:00', 'Pass', 'Re-test after adjustment. All parameters OK.', 3, 10),
('2024-11-10 19:00:00', 'Pass', 'Purity 99.7%, color index within limits', 4, 12),
('2024-11-15 10:00:00', 'Pending', 'Sample collected, analysis in progress', 5, 10),
('2024-11-13 18:00:00', 'Pass', 'Acid value and water content acceptable', 7, 10);

-- 10. Customer (no foreign keys)
INSERT INTO Customer (name, industry, contact_name, phone, email, address) VALUES
('Volkswagen AG', 'Automotive', 'Franz Bauer', '+49-5361-90', 'franz.bauer@volkswagen.de', 'Wolfsburg, Germany'),
('Procter & Gamble', 'Consumer Goods', 'Susan Miller', '+1-513-983-1100', 'susan.miller@pg.com', 'Cincinnati, OH, USA'),
('Henkel AG', 'Chemicals', 'Markus Hoffmann', '+49-211-797-0', 'markus.hoffmann@henkel.com', 'Düsseldorf, Germany'),
('Unilever', 'Consumer Goods', 'Amanda Thompson', '+44-20-7822-5252', 'amanda.thompson@unilever.com', 'London, UK'),
('BMW Group', 'Automotive', 'Stefan Wagner', '+49-89-382-0', 'stefan.wagner@bmw.de', 'Munich, Germany'),
('Tesla Inc', 'Automotive', 'Michael Chang', '+1-512-516-8177', 'michael.chang@tesla.com', 'Austin, TX, USA'),
('LG Chem', 'Electronics', 'Kim Min-jun', '+82-2-3773-1114', 'kim.minjun@lgchem.com', 'Seoul, South Korea'),
('Samsung Electronics', 'Electronics', 'Park Ji-woo', '+82-2-2255-0114', 'park.jiwoo@samsung.com', 'Seoul, South Korea');

-- 11. Sales_Order (foreign key to Customer)
INSERT INTO Sales_Order (order_date, requested_ship_date, status, customer_ID) VALUES
('2024-10-15', '2024-11-05', 'Completed', 1),
('2024-10-20', '2024-11-10', 'Completed', 2),
('2024-10-25', '2024-11-15', 'Shipped', 3),
('2024-11-01', '2024-11-20', 'Pending', 4),
('2024-11-05', '2024-11-25', 'Pending', 5),
('2024-11-10', '2024-12-01', 'Pending', 6),
('2024-10-18', '2024-11-08', 'Completed', 7),
('2024-11-12', '2024-12-05', 'Pending', 8);

-- 12. Order_Line (foreign keys to Sales_Order, Product)
INSERT INTO Order_Line (order_ID, line_num, quantity, unit_price, unit, required_grade, product_ID) VALUES
(1, 1, 15000.00, 1.85, 'kg', 'LDPE-1840', 1),
(1, 2, 5000.00, 2.10, 'kg', 'PP-H301', 2),
(2, 1, 8000.00, 0.95, 'L', '25% Technical', 3),
(3, 1, 12000.00, 3.25, 'kg', 'PA6-B27', 7),
(3, 2, 3000.00, 2.75, 'L', 'MMA-100', 8),
(4, 1, 20000.00, 1.95, 'kg', 'LDPE-1840', 1),
(5, 1, 10000.00, 2.15, 'kg', 'PP-H301', 2),
(5, 2, 7500.00, 4.50, 'L', 'Polymer Grade', 4),
(6, 1, 6000.00, 3.80, 'L', 'Industrial Grade', 5),
(7, 1, 18000.00, 1.90, 'kg', 'LDPE-1840', 1),
(8, 1, 9000.00, 5.20, 'L', '99.5% Pure', 6);
