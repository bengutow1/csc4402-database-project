CREATE TABLE Plant (
  plant_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(100) NOT NULL,
  start_date DATE NOT NULL,
  total_capacity_tons NUMERIC(10,2) NOT NULL, -- of format "32365.25", stores up to 2 decimal spaces
  PRIMARY KEY (plant_ID)
);

CREATE TABLE Unit (
  unit_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  unit_type VARCHAR(20) NOT NULL,
  status ENUM('Active', 'Inactive', 'Maintenance') NOT NULL,
  plant_ID INT NOT NULL, -- Relationship: many Unit tuples to one Plant tuple
  PRIMARY KEY (unit_ID),
  FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID)
);

CREATE TABLE Raw_Material (
  material_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  hazard_class VARCHAR(50),
  physical_state ENUM('Solid', 'Liquid', 'Gas') NOT NULL,
  default_unit VARCHAR(20) NOT NULL,
  unit_ID INT UNIQUE, -- Relationship: one Raw_Material tuple to one Unit tuple 
  PRIMARY KEY (material_ID),
  FOREIGN KEY (unit_ID) REFERENCES Unit(unit_ID)
);

CREATE TABLE Supplier (
  supplier_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100) UNIQUE, -- unique emails enforced
  address VARCHAR(150), -- 150 chars in case address is long
  material_ID INT NOT NULL, -- Relationship: many Supplier tuples to one Raw_Material tuple
  PRIMARY KEY (supplier_ID),
  FOREIGN KEY (material_ID) REFERENCES Raw_Material(material_ID)
);

CREATE TABLE Employee (
  employee_ID INT AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  role VARCHAR(50),
  department VARCHAR(50),
  email VARCHAR(100) UNIQUE, -- unique emails enforced
  hire_date DATE,
  plant_ID INT, -- Relationship: many Employee tuples to one Plant tuple
  PRIMARY KEY (employee_ID),
  FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID)
);

CREATE TABLE Product (
  product_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  grade VARCHAR(50),
  physical_state ENUM('Solid', 'Liquid', 'Gas') NOT NULL,
  hazard_class VARCHAR(50),
  sds_code VARCHAR(50),
  PRIMARY KEY (product_ID)
);
  
CREATE TABLE Batch (
  batch_ID INT AUTO_INCREMENT,
  start_time DATETIME NOT NULL,
  end_time DATETIME, -- can be NULL if batch is still in progress
  target_quantity NUMERIC(10,2) NOT NULL,
  actual_quantity NUMERIC(10,2), -- can be NULL if batch hasn't started production
  status ENUM('Planned', 'In Progress', 'Completed', 'Cancelled') DEFAULT 'Planned',
  unit_ID INT NOT NULL, -- Relationship: many Batch tuples to one Unit tuple
  product_ID INT NOT NULL, -- Relationship: many Batch tuples to one Product tuple
  lead_op_ID INT, -- Lead operator responsible for batch; Relationship: many Batch tuples to one Employee tuple
  PRIMARY KEY (batch_ID),
  FOREIGN KEY (unit_ID) REFERENCES Unit(unit_ID),
  FOREIGN KEY (product_ID) REFERENCES Product(product_ID),
  FOREIGN KEY (lead_op_ID) REFERENCES Employee(employee_ID)
);

CREATE TABLE Batch_Consumption (
  consumption_ID INT AUTO_INCREMENT,
  quantity_used NUMERIC(10,2) NOT NULL, -- can't be NULL, new tuples only added when production starts
  unit VARCHAR(20) NOT NULL,
  batch_ID INT NOT NULL, -- Relationship: many Batch_Consumption tuples to one Batch tuple
  material_ID INT NOT NULL, -- Relationship: many Batch_Consumption tuples to one Raw_Material tuple
  PRIMARY KEY (consumption_ID),
  FOREIGN KEY (batch_ID) REFERENCES Batch(batch_ID),
  FOREIGN KEY (material_ID) REFERENCES Raw_Material(material_ID)
);

CREATE TABLE Quality_Test (
  test_ID INT AUTO_INCREMENT,
  sample_time DATETIME NOT NULL, -- When the test was performed
  result_status ENUM('Pass', 'Fail', 'Pending') DEFAULT 'Pending', -- set default to "Pending" upon new test request
  comments TEXT, -- using TEXT type to allow for variable-length comments
  batch_ID INT NOT NULL, -- Relationship: many Quality_Test tuples to one Batch tuple
  performed_by INT, -- ID of the employee assigned to perform the test; Relationship: many Quality_Test tuples to one Employee tuple
  PRIMARY KEY (test_ID),
  FOREIGN KEY (batch_ID) REFERENCES Batch(batch_ID),
  FOREIGN KEY (performed_by) REFERENCES Employee(employee_ID)
);

CREATE TABLE Customer (
  customer_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  industry VARCHAR(50),
  contact_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(100) UNIQUE,
  address VARCHAR(150),
  PRIMARY KEY (customer_ID)
);

CREATE TABLE Sales_Order (
  order_ID INT AUTO_INCREMENT,
  order_date DATE NOT NULL,
  requested_ship_date DATE,
  status ENUM('Pending', 'Shipped', 'Completed', 'Cancelled') DEFAULT 'Pending',
  customer_ID INT NOT NULL,
  PRIMARY KEY (order_ID),
  FOREIGN KEY (customer_ID) REFERENCES Customer(customer_ID)
);

CREATE TABLE Order_Line (
  order_ID INT NOT NULL,
  line_num INT NOT NULL, -- sequence number within the order, each line in an order corresponds to a specific product
  quantity NUMERIC(10,2) NOT NULL,
  unit_price NUMERIC(10,2) NOT NULL,
  unit VARCHAR(20) NOT NULL,
  required_grade VARCHAR(50),
  product_ID INT NOT NULL,
  PRIMARY KEY (order_ID, line_num),
  FOREIGN KEY (order_ID) REFERENCES Sales_Order(order_ID),
  FOREIGN KEY (product_ID) REFERENCES Product(product_ID)
);
