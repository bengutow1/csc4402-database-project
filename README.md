# CSC4402 Database Management Final Project

---

## How to run the application user interface code:

First, ensure that your MySQL Server is running and you meet the following requirements:
* Python 3.11+ (or 3.x)
* mysql-connector-python (version >= 8.0.33)
  * Install with: pip install mysql-connector-python==8.0.33
  * If the program fails to authenticate MySQL credentials, you may need to fully uninstall the ```mysql```, ```mysql-connector```, and ```mysql-connector-python``` Python packages

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
Provided logins:
* User-level Permissions
 * Username: **user**
 * Password: **user123**
* Admin-level Permissions
 * Username **admin**
 * Password: **admin123**

Now, you are logged in and ready to use application's features!

## Application User Interface Features
+ User-level Permissions:
 + List and Modify (Limited) Quality Tests
 + List and Modify (Limited) Orders
 + List, Modify (Limited) and Create Order Lines of an Order
 + Execute Provided Test Queries (located in ```database/test_query.sql```)
+ Admin-level Permissions:
 + List, Modify, Create, and Delete Quality Tests
 + List, Modify, Create, and Delete Orders
 + List, Modify, Create, and Delete Order Lines of an Order
 + List, Modify, Create, and Delete Customers
 + List, Modify, Create, and Delete Employees
 + List, Modify, Create, and Delete Products
 + Execute Provided Test Queries (located in ```database/test_query.sql```)

--

##How to run the database in MySQL (stand-alone)

Start up your MySQL server and log in through preferred program (MySQL Workbench, for example)

To create a new database, in MySQL, run:
```bash
CREATE DATABASE <database_name>;
USE <database_name>;
```

Then, copy and paste the SQL queries in ```database/schema.sql``` into MySQL.

And add the data in by copying and pasting the queries in ```database/data.sql``` into MySQL.

Now, the database schema is set up and data is inserted. The test queries in ```database/test_query.sql``` can be run.

# csc4402-database-project
Database group project for CSC4402 - Database Management class

TEMPORARY READ ME AS A BRIEF EXPLANATION OF HOW TO RUN:

Requirements:
* Python 3.11+ (or 3.x)
* mysql-connector-python >= 8.0.33
  * Install with: pip install mysql-connector-python==8.0.33

Ensure that your MySQL Server is running.
After cloning the repository, step into the src/ directory and Open in Terminal
Type the command ```python main.py``` to Launch the Program

Input your MySQL Information (If you have a local default MySQL install, you should be able to use the default host and user)
Enter the database name (You can just press enter for default: basf)

Log in, there are two logins at first but you can add more by adding new rows into the data/users.csv file
User-Level Permissions:
* Username: user
* Password: user123
Admin-Level Permissions
* Username: admin
* Password: admin123

Navigate through the menu using the commands. There are two permission levels, will elaborate more on which can do what tomorrow prolly.


