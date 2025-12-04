# CSC4402 Database Management Final Project

---

## Report

The report and ER Diagram can be found in the ```/report/``` folder.

---

## How to run the application user interface code:

First, ensure that your MySQL Server is running and you meet the following requirements:
* Python 3.11+ (or 3.x)
* mysql-connector-python (version >= 8.0.33)
  * Install with:
  ```bash
  pip install mysql-connector-python==8.0.33
  ```
  * If the program fails to authenticate MySQL credentials, you may need to fully uninstall the ```mysql```, ```mysql-connector```, and ```mysql-connector-python``` Python packages and reinstall the correct version!

Open the downloaded project folder in Terminal.

Step into the ```/src/``` folder:
```bash
cd src
```

Run the main module with:
```bash
python main.py
```

Input your MySQL Information (If your MySQL Server is running locally, you should be able to use the default host (localhost) and user (root)).

Enter a database name (You can also press enter to use the default (basf)).

Login with whichever user you prefer to use. There are two logins provided in the ```data/users.csv``` file, but you can add more by modifying the file and adding a new row.
### Provided logins:
### User-level Permissions Login
 + Username: **user**
 + Password: **user123**
### Admin-level Permissions Login
 + Username **admin**
 + Password: **admin123**

Now, you are logged in and ready to use application's features!

## Application User Interface Features
### User-level Permissions:
 + List and Modify (Limited) Quality Tests
 + List and Modify (Limited) Orders
 + List, Modify (Limited) and Create Order Lines of an Order
 + Execute Provided Test Queries (located in ```database/test_query.sql```)
### Admin-level Permissions:
 + List, Modify, Create, and Delete Quality Tests
 + List, Modify, Create, and Delete Orders
 + List, Modify, Create, and Delete Order Lines of an Order
 + List, Modify, Create, and Delete Customers
 + List, Modify, Create, and Delete Employees
 + List, Modify, Create, and Delete Products
 + Execute Provided Test Queries (located in ```database/test_query.sql```)

---

## How to run the database in MySQL (stand-alone)

Start up your MySQL server and log in through preferred database management tool (MySQL Workbench, for example)

To create a new database, in MySQL, run:
```bash
CREATE DATABASE <database_name>;
USE <database_name>;
```

Copy and paste the SQL queries in ```database/schema.sql``` into your database management tool.

Copy and paste the SQL queries in ```database/data.sql``` to add the data into the MySQL database.

Now, the database schema is set up and data is inserted. The test queries in ```database/test_query.sql``` can be run.

---

## How to execute test queries

Launch the python program and run using the directions above.

Once you're logged in, press the key associated with the **Execute Database Test Queries** command.

You will be given a description of a test query, press **Enter** to run it. The results will be printed, and after pressing **Enter** again, you will be prompted with the next test query until all of them are executed.

The actual SQL queries being ran are located in ```database/test_query.sql```. The Python program reads the file and executes each query one at a time.

### Note: If you update any of the data, the outcomes of the queries may not match the provided outcomes in the report.


