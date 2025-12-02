from mysql.connector import Error

def print_customers(cursor):
    """
    Lists all customers
    
    Takes one parameter:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    try:
        cursor.execute("SELECT customer_ID, name, industry, contact_name, phone, email, address FROM Customer")
        rows = cursor.fetchall()
        print("\nListing all Customers...")
        for row in rows:
            print(f"\nCustomer ID: {row[0]}, Customer Name: {row[1]}, Industry: {row[2]}")
            print(f"Contact Name: {row[3]}, Phone: {row[4]}, Email: {row[5]}")
            print(f"Address: {row[6]}")
    
    except Error as e:
        print(f"Error listing Customers: {e}")
        
def modify_customer(cnx, cursor):
    """
    Modify a customer
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the customer ID
    customer_id = input("\nEnter the Customer ID to modify: ").strip()
    if not customer_id.isdigit():
        print("Invalid Customer ID!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    new_name = input("\nEnter new Customer Name: ").strip()
    new_industry = input("\nEnter new Industry: ").strip()
    new_contact = input("\nEnter new Contact Name: ").strip()
    new_phone = input("\nEnter new Phone Number: ").strip()
    new_email = input("\nEnter new Email: ").strip()
    new_address = input("\nEnter new Address: ").strip()
    
    #Building query
    sets = []
    vals = []
    
    if new_name:
        sets.append("name = %s")
        vals.append(new_name)
    
    if new_industry:
        sets.append("industry = %s")
        vals.append(new_industry)
        
    if new_contact:
        sets.append("contact_name = %s")
        vals.append(new_contact)
        
    if new_phone:
        sets.append("phone = %s")
        vals.append(new_phone)
        
    if new_email:
        sets.append("email = %s")
        vals.append(new_email)
        
    if new_address:
        sets.append("address = %s")
        vals.append(new_address)
        
    vals.append(customer_id)    #append customer ID for the WHERE clause
    set_clause = ", ".join(sets)      #join all the set clauses together
        
    query = f"UPDATE Customer SET {set_clause} WHERE customer_ID = %s;"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nCustomer with ID {customer_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Customer: {e}")
        
def create_customer(cnx, cursor):
    """
    Create a customer
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """

    print("\nCreating a new Customer...")
    
    name = input("\nEnter the Customer Name: ").strip()
    industry = input("\nEnter the Industry: ").strip()
    contact = input("\nEnter the Contact Name: ").strip()
    phone = input("\nEnter the Phone Number: ").strip()
    email = input("\nEnter the Email: ").strip()
    address = input("\nEnter the Address: ").strip()
    
    #Building query using vals array
    vals = []
    
    vals.append(name)
    vals.append(industry)
    vals.append(contact)
    vals.append(phone)
    vals.append(email)
    vals.append(address)
        
    query = """INSERT INTO Customer
    (name, industry, contact_name, phone, email, address) VALUES
    (%s, %s, %s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nCustomer created successfully!")
    except Error as e:
        print(f"\nError creating Customer: {e}")
        
def delete_customer(cnx, cursor):
    """
    Delete a customer
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the customer ID
    customer_id = input("\nEnter the Customer ID to delete: ").strip()
    
    query = "DELETE FROM Customer WHERE customer_ID = %s;"
    
    try:
        cursor.execute(query, (customer_id,))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Customer found with ID {customer_id}!")
        else:
            print(f"\nCustomer with ID {customer_id} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Customer: {e}")

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
        print_customers(cursor)
    elif selection == 2:
        modify_customer(cnx, cursor)
    elif selection == 3:
        create_customer(cnx, cursor)
    elif selection == 4:
        delete_customer(cnx, cursor)
    elif (selection == 5):
        print("\nReturning to main menu...")
        return False
    else:
        print("\nIncorrect input!")
        
    return True

def manage_customers(cnx, cursor):
    """
    Full menu and commands for managing customers (admin command)

    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing

    """
    
    while True:
        print("\nCustomer Management MENU:")
        print("1) Print Customers")
        print("2) Modify Customer")
        print("3) Create Customer")
        print("4) Delete Customer")
        print("5) Return to Main Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            if not select(selection, cnx, cursor):
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        