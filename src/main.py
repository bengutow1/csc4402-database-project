import sys
import mysql.connector
from mysql.connector import Error

#Methods/modules imported from local .py files
import login_manager
from sql_executor import execute_sql_file
from quality_test_manager import manage_quality_tests
from order_manager import manage_orders
from customer_manager import manage_customers
from employee_manager import manage_employees
from product_manager import manage_products
from test_query_executor import execute_test_queries

"""
author: Benjamin Gutowski

Created on: 12/1/2025
"""

#Load login information into logins dictionary
logins = login_manager.load_login_info()

def sql_prompt():
    """
    Prompts the user everything necessary to establish a MySQL connection and create a database
    
    Takes no parameters
    
    Returns:
        connector - object that connects Python with MySQL
        cursor - object that points to the database, allows execution of SQL queries
    
    """
    
    cnx = None
    
    while True:
        print("Establishing connection with MySQL Server...")
        
        #Prompt the user for MySQL information
        sql_host = input("Enter MySQL host (default is 'localhost'): ") or "localhost"
        sql_user = input("Enter MySQL username (default is 'root'): ") or "root"
        sql_password = input("Enter MySQL password: ")
        
        #Attempt to establish connection
        try:
            cnx = mysql.connector.connect(host=sql_host,
                                          user=sql_user,
                                          password=sql_password,
                                          auth_plugin='mysql_native_password')
            
            print(f"Successfully connected to {sql_host}\n")
            break
        
        except Error as e:
            print(f"\nError: {e}")
            print("Check your MySQL information and try again!\n")
            
    cursor = cnx.cursor()
        
    while True:
        try:
            sql_db_name = input("Enter a name for the database (default is basf): ") or "basf"
            
            #Drop database and create a new one, then use it
            cursor.execute(f"DROP DATABASE IF EXISTS {sql_db_name};")
            cursor.execute(f"CREATE DATABASE {sql_db_name};")
            cursor.execute(f"USE {sql_db_name};")
            
            print(f"Successfully using database {sql_db_name}\n")
            break;
        
        except Error as e:
            print(f"\nError: {e}")
            print("There was a problem creating and using the database, try again!\n")
        
    return cnx, cursor
        
def login_prompt():
    """
    Prompts the user to login
    
    Takes no parameters
    
    Returns:
        int - 1 if login has admin permissions, 0 if not
        
    """
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        success, perms = login_manager.check_login(username, password, logins)
        if success:
            return perms

def menu_display(admin_access):
    """
    Displays the menu for the user
    
    Takes one parameter:
        admin_access : int - 1 if user has admin permissions, 0 if not
        
    Returns nothing
    
    """
    
    if (admin_access == 1):
        #admin-level menu
        print("\nAdmin MENU:")
        print("1) Manage Quality Tests")
        print("2) Manage Orders")
        print("3) Manage Customers")
        print("4) Manage Employees")
        print("5) Manage Products")
        print("6) Execute Database Test Queries")
        print("7) Exit Program")
        
    else:
        #user-level menu
        print("\nUser MENU:")
        print("1) Manage Quality Tests")
        print("2) Manage Orders")
        print("3) Execute Database Test Queries")
        print("4) Exit Program")
    
#Performs the selected menu operation
def select(selection, cnx, cursor, perms):
    """
    Selects and performs a menu command.
    
    Takes four parameters:
        selection : int - integer corresponding to chosen command
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        
    Returns nothing
    """
    
    if selection == 1:
        print("\nEntering Quality Test Management Menu:")
        manage_quality_tests(cnx, cursor, perms)
    elif selection == 2:
        print("\nEntering Order Management Menu:")
        manage_orders(cnx, cursor, perms)
    elif selection == 3:
        if (perms == 1):
            manage_customers(cnx, cursor)
        else:
            execute_test_queries("../database/test_query.sql", cnx, cursor)
    elif selection == 4:
        if (perms == 1):
            manage_employees(cnx, cursor)
        else:
            print("\nExiting the program...")
            sys.exit(0)
    elif selection == 5 and perms == 1:
        manage_products(cnx, cursor)
    elif selection == 6 and perms == 1:
        execute_test_queries("../database/test_query.sql", cnx, cursor)
    elif selection == 7 and perms == 1:
        print("\nExiting the program...")
        sys.exit(0)
    else:
        print("\nIncorrect input!")

#Main function
def main():
    
    #Establish connection with a MySQL server
    cnx, cursor = sql_prompt()
    execute_sql_file("../database/schema.sql", cnx, cursor)
    execute_sql_file("../database/data.sql", cnx, cursor)
    
    #Set to 1 if admin access, 0 if not
    perms = login_prompt()
    
    while True:
        menu_display(perms)
        try:
            if perms == 1:
                selection = int(input("\nEnter a command number (1 - 7): "))
            else:
                selection = int(input("\nEnter a command number (1 - 4): "))
            select(selection, cnx, cursor, perms)
        except ValueError:
            print("\nIncorrect input!")

if __name__ == "__main__":
    main()