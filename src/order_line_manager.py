from mysql.connector import Error

def print_order_lines(cursor, order_id):
    """
    Lists all order lines within an order
    
    Takes 2 parameters:
        cursor: cursor object - object that points to the database, used to execute commands
        order_id : string - string of order ID for order line management
        
    Returns nothing
    """
    
    query = """SELECT line_num, quantity, unit_price, unit, required_grade, product_ID
                   FROM Order_Line WHERE order_ID = %s"""
    
    try:
        cursor.execute(query, (order_id,))
        rows = cursor.fetchall()
        print(f"\nListing all Order Lines in Order ID {order_id}...")
        for row in rows:
            print(f"\nLine Number: {row[0]}")
            print(f"Product ID: {row[5]}, Required Grade: {row[4]}")
            print(f"Quantity: {row[1]}, Unit {row[3]}, Unit Price: ${row[2]}")
    
    except Error as e:
        print(f"Error listing Orders: {e}")
        
def modify_order_line(cnx, cursor, perms, order_id):
    """
    Modify an order line
    
    Takes 4 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        order_id : string - string of order ID for order line management
        
    Returns nothing
    """
    #Get the line number
    line_num = input("\nEnter the Line Number to modify: ").strip()
    if not line_num.isdigit():
        print("Invalid Line Number!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    new_quantity = input("\nEnter new Quantity: ").strip()
    
    #only admins can modify these :P
    if (perms == 1):
        new_unit = input("\nEnter new Unit: ").strip()
        new_unit_price = input("\nEnter new Unit Price: ").strip()
        new_grade = input("\nEnter new Required Grade: ").strip()
        new_product = input("\nEnter ID of new Product: ").strip()
    else:
        new_unit = ""   #will test false
        new_unit_price = ""
        new_grade = ""
        new_product = ""
    
    #Building query
    sets = []
    vals = []
    
    if new_quantity:
        sets.append("quantity = %s")
        vals.append(new_quantity)
    
    if new_unit_price:
        sets.append("unit_price = %s")
        vals.append(new_unit_price)
        
    if new_unit:
        sets.append("unit = %s")
        vals.append(new_unit)
        
    if new_grade:
        sets.append("required_grade = %s")
        vals.append(new_grade)
    
    if new_product:
        sets.append("product_ID = %s")
        vals.append(new_product)
        
    vals.append(order_id)    #append order ID for the WHERE clause
    vals.append(line_num)
    set_clause = ", ".join(sets)      #join all the set statements together
        
    query = f"UPDATE Order_Line SET {set_clause} WHERE order_ID = %s AND line_num = %s"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nLine Number {line_num} of Order ID {order_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Line Number: {e}")
        
def create_order_line(cnx, cursor, order_id):
    """
    Create an order line
    
    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        order_id : string - string of order ID for order line management
        
    Returns nothing
    """

    query = "SELECT MAX(line_num) FROM Order_Line WHERE order_ID = %s;"
    line_num = 1

    try:
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        if not result is None:
            line_num = int(result[0]) + 1
    except Error as e:
        print(f"\nError getting maximum Line Number: {e}")
        return
    
    print("\nCreating a new Order Line...")
    
    product_id = input("\nEnter the ID of the Product: ").strip()
    grade = input("\nEnter the Required Grade: ").strip()
    quantity = input("\nEnter the Quantity: ").strip()
    unit = input("\nEnter the Unit: ").strip()
    unit_price = input("\nEnter the Unit Price: ").strip()
    
    #Building query using vals array
    vals = []
    
    vals.append(order_id)
    vals.append(line_num)
    vals.append(quantity)
    vals.append(unit_price)
    vals.append(unit)
    vals.append(grade)
    vals.append(product_id)
        
    query = """INSERT INTO Order_Line
    (order_ID, line_num, quantity, unit_price, unit, required_grade, product_ID) VALUES
    (%s, %s, %s, %s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nOrder Line created successfully!")
    except Error as e:
        print(f"\nError creating Order Line: {e}")
        
def delete_order_line(cnx, cursor, order_id):
    """
    Delete an order
    
    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        order_id : string - string of order ID for order line management
        
    Returns nothing
    """
    
    #Get the line number
    line_num = input("Enter the Line Number to delete: ").strip()
    
    query = "DELETE FROM Order_Line WHERE order_ID = %s AND line_num = %s;"
    
    try:
        cursor.execute(query, (order_id, line_num))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Order Line found with Line Number {line_num}!")
        else:
            print(f"\nOrder Line Number {line_num} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Order Line Number: {e}")
        
def change_order(cursor):
    """
    Changes the order ID being used in the order line management menu

    Takes 1 parameters:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing

    """
    #Get the order ID
    order_id = input("Enter the new Order ID: ").strip()
    
    query = "SELECT order_ID FROM Sales_Order WHERE order_ID = %s;"
    
    try:
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        
        if result is None:    #When no order was found
            print(f"\nNo Order found with ID {order_id}!")
        else:
            print(f"\nChanged Current Order to ID: {order_id}")
            return order_id
    except Exception as e:
        print(f"\nError searching for Order: {e}")

def select(selection, cnx, cursor, perms, order_id):
    """
    Selects and performs a menu command.
    
    Takes 5 parameters:
        selection : int - integer corresponding to chosen command
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        order_id : string - string of order ID for order line management
        
    Returns:
        false if leaving current management menu,
        the current order ID (in case of change)
    """
    
    if selection == 1:
        new_order_id = change_order(cursor)
        if not new_order_id is None:
            order_id = new_order_id
    elif selection == 2:
        print_order_lines(cursor, order_id)
    elif selection == 3:
        modify_order_line(cnx, cursor, perms, order_id)
    elif selection == 4:
        create_order_line(cnx, cursor, order_id)
    elif selection == 5:
        if (perms == 0):    #Return-to-menu command for user level permissions
            print("\nReturning to Order Management menu...")
            return False, order_id
        delete_order_line(cnx, cursor, order_id)
    elif (selection == 6 and perms == 1):
        print("\nReturning to Order Management menu...")
        return False, order_id
    else:
        print("\nIncorrect input!")
        
    return True, order_id

def manage_order_lines(cnx, cursor, perms, order_id):
    """
    Full menu and commands for managing order lines

    Takes 4 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 for admin permissions, 0 for user-level permissions
        order_id : string - string of the order_id to manage order lines of
        
    Returns nothing

    """
    
    while True:
        print("\nOrder Line Management MENU:")
        print(f"Current Order ID: {order_id}\n")
        print("1) Change Order ID")
        print("2) Print Order Lines")
        print("3) Modify Order Line")
        print("4) Create Order Line")
        if (perms == 0):
            print("5) Return to Order Management Menu")
        else:
            print("5) Delete Order Line")
            print("6) Return to Order Management Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            menu_break, order_id = select(selection, cnx, cursor, perms, order_id)
            if not menu_break:      #Returning to previous menu
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        