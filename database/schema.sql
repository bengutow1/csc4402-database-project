DROP DATABASE IF EXISTS basf_db;
CREATE DATABASE basf_db;
USE basf_db;

CREATE TABLE Plant (
  plant_ID INT AUTO_INCREMENT
  name VARCHAR(100) NOT NULL,
  location VARCHAR(100) NOT NULL,
  start_date DATE NOT NULL,
  total_capacity_tons NUMERIC(10,2) NOT NULL, -- of format "32365.25", stores up to 2 decimal spaces
  PRIMARY KEY (plant_ID)
);

CREATE TABLE Unit (
  unit_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  unit_type VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL,
  plant_ID INT NOT NULL, -- Relationship: many Unit tuples to one Plant tuple
  PRIMARY KEY (unit_ID),
  FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID)
);

CREATE TABLE Raw_Material (
  material_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  hazard_class VARCHAR(50),
  physical_state VARCHAR(10) NOT NULL, -- solid, liquid, or gas
  default_unit VARCHAR(10) NOT NULL,
  unit_ID INT UNIQUE, -- Relationship: one Raw_Material tuple to one Unit tuple 
  PRIMARY KEY (material_ID),
  FOREIGN KEY (unit_ID) REFERENCES Unit(unit_ID)
);

CREATE TABLE Supplier (
  supplier_ID INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100),
  phone_number VARCHAR(20),
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
  physical_state VARCHAR(10) NOT NULL,
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
  status VARCHAR(50),
  unit_ID INT NOT NULL, -- Relationship: many Batch tuples to one Unit tuple
  product_ID INT NOT NULL, -- Relationship: many Batch tuples to one Product tuple
  lead_op_ID INT, -- Lead operator responsible for batch; Relationship: many Batch tuples to one Employee tuple
  PRIMARY KEY (batch_ID),
  FOREIGN KEY (unit_ID) REFERENCES Unit(unit_ID),
  FOREIGN KEY (product_ID) REFERENCES Product(product_ID),
  FOREIGN KEY (lead_op_ID) REFERENCES Employee(employee_ID)
);



