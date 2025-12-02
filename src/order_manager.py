from mysql.connector import Error
from order_line_manager import manage_order_lines

def print_orders(cursor):
    """
    Lists all orders
    
    Takes one parameter:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    try:
        cursor.execute("SELECT order_ID, order_date, requested_ship_date, status, customer_ID FROM Sales_Order")
        rows = cursor.fetchall()
        print("\nListing all Orders...")
        for row in rows:
            print(f"\nOrder ID: {row[0]}, Customer ID: {row[4]}")
            print(f"Order Date: {row[1]}, Requested Ship Date: {row[2]}")
            print(f"Status: {row[3]}")
    
    except Error as e:
        print(f"Error listing Orders: {e}")
        
def modify_order(cnx, cursor, perms):
    """
    Modify an order
    
    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        
    Returns nothing
    """
    #Get the order ID
    order_id = input("\nEnter the Order ID to modify: ").strip()
    if not order_id.isdigit():
        print("Invalid Order ID!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    new_date = input("\nEnter new Order Date (YYYY-MM-DD HH:MM:SS): ").strip()
    new_ship_date = input("\nEnter new Requested Ship Date (YYYY-MM-DD HH:MM:SS): ").strip()
    new_status = input("\nEnter new Status (Pending/Shipped/Completed/Cancelled): ").strip()
    
    #only admins can change the customer ID
    if (perms == 1):
        new_customer = input("\nEnter new Customer ID: ").strip()
    else:
        new_customer = ""   #will test false
    
    #Building query
    sets = []
    vals = []
    
    if new_date:
        sets.append("order_date = %s")
        vals.append(new_date)
    
    if new_ship_date:
        sets.append("requested_ship_date = %s")
        vals.append(new_ship_date)
        
    if new_status:
        sets.append("status = %s")
        vals.append(new_status)
        
    if new_customer:
        sets.append("customer_ID = %s")
        vals.append(new_customer)
        
    vals.append(order_id)    #append order ID for the WHERE clause
    set_clause = ", ".join(sets)      #join all the set statements together
        
    query = f"UPDATE Sales_Order SET {set_clause} WHERE order_ID = %s"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nOrder with ID {order_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Order: {e}")
        
def create_order(cnx, cursor):
    """
    Create an order (admin command)
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """

    print("\nCreating a new Order...")
    
    customer_id = input("\nEnter the ID of the Customer: ").strip()
    order_date = input("\nEnter the Order Date (YYYY-MM-DD HH:MM:SS): ").strip()
    ship_date = input("\nEnter the Requested Ship Date (YYYY-MM-DD HH:MM:SS): ").strip()
    status = input("\nEnter the Status (Pending/Shipped/Completed/Cancelled) (Default: Pending): ").strip() or "Pending"
    
    #Building query using vals array
    vals = []
    
    vals.append(order_date)
    vals.append(ship_date)
    vals.append(status)
    vals.append(customer_id)
        
    query = """INSERT INTO Sales_Order
    (order_date, requested_ship_date, status, customer_ID) VALUES
    (%s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nOrder created successfully!")
    except Error as e:
        print(f"\nError creating Order: {e}")
        
def delete_order(cnx, cursor):
    """
    Delete an order
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    print("\nWARNING: Deleting an order will delete its order lines!")
    
    #Get the order ID
    order_id = input("Enter the Order ID to delete: ").strip()
    
    query = "DELETE FROM Sales_Order WHERE order_ID = %s;"
    
    try:
        cursor.execute(query, (order_id,))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Order found with ID {order_id}!")
        else:
            print(f"\nOrder with ID {order_id} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Order: {e}")
        
def order_line_module(cnx, cursor, perms):
    """
    Gets an order ID and passes it through to the order_line_manager module

    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 for admin permissions, 0 for user-level permissions
        
    Returns nothing

    """
    #Get the order ID
    order_id = input("Enter the Order ID to manage: ").strip()
    
    query = "SELECT order_ID FROM Sales_Order WHERE order_ID = %s;"
    
    try:
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        
        if result is None:    #When no order was found
            print(f"\nNo Order found with ID {order_id}!")
        else:
            manage_order_lines(cnx, cursor, perms, order_id)
    except Exception as e:
        print(f"\nError searching for Order: {e}")

def select(selection, cnx, cursor, perms):
    """
    Selects and performs a menu command.
    
    Takes 4 parameters:
        selection : int - integer corresponding to chosen command
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        
    Returns false if leaving current management menu
    """
    
    if selection == 1:
        print_orders(cursor)
    elif selection == 2:
        modify_order(cnx, cursor, perms)
    elif selection == 3:
        if (perms == 0):
            order_line_module(cnx, cursor, perms)
        else:
            create_order(cnx, cursor)
    elif selection == 4:
        if (perms == 0):    #Return-to-menu command for user level permissions
            print("\nReturning to main menu...")
            return False
        delete_order(cnx, cursor)
    elif selection == 5 and perms == 1:
        order_line_module(cnx, cursor, perms)
    elif (selection == 6 and perms == 1):
        print("\nReturning to main menu...")
        return False
    else:
        print("\nIncorrect input!")
        
    return True

def manage_orders(cnx, cursor, perms):
    """
    Full menu and commands for managing orders

    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 for admin permissions, 0 for user-level permissions
        
    Returns nothing

    """
    
    while True:
        print("\nOrder Management MENU:")
        print("1) Print Orders")
        print("2) Modify Order")
        if (perms == 0):
            print("3) Manage Order Lines")
            print("4) Return to Main Menu")
        else:
            print("3) Create Order")
            print("4) Delete Order")
            print("5) Manage Order Lines")
            print("6) Return to Main Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            if not select(selection, cnx, cursor, perms):
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        