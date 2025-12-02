from mysql.connector import Error

def print_products(cursor):
    """
    Lists all products
    
    Takes one parameter:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    try:
        cursor.execute("SELECT product_ID, name, grade, physical_state, hazard_class, sds_code FROM Product")
        rows = cursor.fetchall()
        print("\nListing all Products...")
        for row in rows:
            print(f"\nProduct ID: {row[0]}, Product Name: {row[1]}")
            print(f"Grade: {row[2]}, Physical State: {row[3]}")
            print(f"Hazard Class: {row[4]}, SDS Code: {row[5]}")
    except Error as e:
        print(f"Error listing Products: {e}")
        
def modify_product(cnx, cursor):
    """
    Modify a product
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the product ID
    product_id = input("\nEnter the Product ID to modify: ").strip()
    if not product_id.isdigit():
        print("Invalid Product ID!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    name = input("\nEnter new Product Name: ").strip()
    grade = input("\nEnter new Grade: ").strip()
    physical_state = input("\nEnter new Physical State (Solid/Liquid/Gas): ").strip()
    hazard_class = input("\nEnter new Hazard Class: ").strip()
    sds = input("\nEnter new SDS Code: ").strip()
    
    #Building query
    sets = []
    vals = []
    
    if name:
        sets.append("name = %s")
        vals.append(name)
    
    if grade:
        sets.append("grade = %s")
        vals.append(grade)
        
    if physical_state:
        sets.append("physical_state = %s")
        vals.append(physical_state)
        
    if hazard_class:
        sets.append("hazard_class = %s")
        vals.append(hazard_class)
        
    if sds:
        sets.append("sds_code = %s")
        vals.append(sds)
        
    vals.append(product_id)    #append product ID for the WHERE clause
    set_clause = ", ".join(sets)      #join all the set clauses together
        
    query = f"UPDATE Product SET {set_clause} WHERE product_ID = %s;"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nProduct with ID {product_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Product: {e}")
        
def create_product(cnx, cursor):
    """
    Create a product
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """

    print("\nCreating a new Product...")
    
    name = input("\nEnter the Product Name: ").strip()
    grade = input("\nEnter the Grade: ").strip()
    physical_state = input("\nEnter the Physical State (Solid/Liquid/Gas): ").strip()
    hazard_class = input("\nEnter the Hazard Class: ").strip()
    sds = input("\nEnter the SDS Code: ").strip()
    
    #Building query using vals array
    vals = []
    
    vals.append(name)
    vals.append(grade)
    vals.append(physical_state)
    vals.append(hazard_class)
    vals.append(sds)
        
    query = """INSERT INTO Product
    (name, grade, physical_state, hazard_class, sds_code) VALUES
    (%s, %s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nProduct created successfully!")
    except Error as e:
        print(f"\nError creating Product: {e}")
        
def delete_product(cnx, cursor):
    """
    Delete a product
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the product ID
    product_id = input("\nEnter the product ID to delete: ").strip()
    
    query = "DELETE FROM Product WHERE product_ID = %s;"
    
    try:
        cursor.execute(query, (product_id,))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Product found with ID {product_id}!")
        else:
            print(f"\nProduct with ID {product_id} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Product: {e}")

def select(selection, cnx, cursor):
    """
    Selects and performs a menu command.
    
    Takes 3 parameters:
        selection : int - integer corresponding to chosen command
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns false if leaving current management menu
    """
    
    if selection == 1:
        print_products(cursor)
    elif selection == 2:
        modify_product(cnx, cursor)
    elif selection == 3:
        create_product(cnx, cursor)
    elif selection == 4:
        delete_product(cnx, cursor)
    elif (selection == 5):
        print("\nReturning to main menu...")
        return False
    else:
        print("\nIncorrect input!")
        
    return True

def manage_products(cnx, cursor):
    """
    Full menu and commands for managing products (admin command)

    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing

    """
    
    while True:
        print("\nProduct Management MENU:")
        print("1) Print Products")
        print("2) Modify Product")
        print("3) Create Product")
        print("4) Delete Product")
        print("5) Return to Main Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            if not select(selection, cnx, cursor):
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        