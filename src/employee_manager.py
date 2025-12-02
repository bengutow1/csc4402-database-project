from mysql.connector import Error

def print_employees(cursor):
    """
    Lists all employees
    
    Takes one parameter:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    try:
        cursor.execute("SELECT employee_ID, first_name, last_name, role, department, email, hire_date, plant_ID FROM Employee")
        rows = cursor.fetchall()
        print("\nListing all Employees...")
        for row in rows:
            print(f"\nEmployee ID: {row[0]}, Name: {row[1]} {row[2]}, Plant ID: {row[7]}")
            print(f"Role: {row[3]}, Department: {row[4]}, Email: {row[5]}")
            print(f"Hire Date: {row[6]}")
    
    except Error as e:
        print(f"Error listing Employees: {e}")
        
def modify_employee(cnx, cursor):
    """
    Modify an employee
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the employee ID
    employee_id = input("\nEnter the Employee ID to modify: ").strip()
    if not employee_id.isdigit():
        print("Invalid Employee ID!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    first_name = input("\nEnter new First Name: ").strip()
    last_name = input("\nEnter new Last Name: ").strip()
    role = input("\nEnter new Role: ").strip()
    department = input("\nEnter new Department: ").strip()
    email = input("\nEnter new Email: ").strip()
    hire_date = input("\nEnter new Hire Date (YYYY-MM-DD): ").strip()
    plant_id = input("\nEnter new Plant ID the Employee Works at: ").strip()
    
    #Building query
    sets = []
    vals = []
    
    if first_name:
        sets.append("first_name = %s")
        vals.append(first_name)
    
    if last_name:
        sets.append("last_name = %s")
        vals.append(last_name)
        
    if role:
        sets.append("role = %s")
        vals.append(role)
        
    if department:
        sets.append("department = %s")
        vals.append(department)
        
    if email:
        sets.append("email = %s")
        vals.append(email)
        
    if hire_date:
        sets.append("hire_date = %s")
        vals.append(hire_date)
    
    if plant_id:
        sets.append("plant_ID = %s")
        vals.append(plant_id)
        
    vals.append(employee_id)    #append employee ID for the WHERE clause
    set_clause = ", ".join(sets)      #join all the set clauses together
        
    query = f"UPDATE Employee SET {set_clause} WHERE employee_ID = %s;"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nEmployee with ID {employee_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Employee: {e}")
        
def create_employee(cnx, cursor):
    """
    Create an employee
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """

    print("\nCreating a new Employee...")
    
    first_name = input("\nEnter the First Name: ").strip()
    last_name = input("\nEnter the Last Name: ").strip()
    role = input("\nEnter the Role: ").strip()
    department = input("\nEnter the Department: ").strip()
    email = input("\nEnter the Email: ").strip()
    hire_date = input("\nEnter the Hire Date (YYYY-MM-DD: ").strip()
    plant_id = input("\nEnter the Plant ID the Employee works at: ").strip()
    
    #Building query using vals array
    vals = []
    
    vals.append(first_name)
    vals.append(last_name)
    vals.append(role)
    vals.append(department)
    vals.append(email)
    vals.append(hire_date)
    vals.append(plant_id)
        
    query = """INSERT INTO Employee
    (first_name, last_name, role, department, email, hire_date, plant_ID) VALUES
    (%s, %s, %s, %s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nEmployee created successfully!")
    except Error as e:
        print(f"\nError creating Employee: {e}")
        
def delete_employee(cnx, cursor):
    """
    Delete an employee
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the employee ID
    employee_id = input("\nEnter the Employee ID to delete: ").strip()
    
    query = "DELETE FROM Employee WHERE employee_ID = %s;"
    
    try:
        cursor.execute(query, (employee_id,))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Employee found with ID {employee_id}!")
        else:
            print(f"\nEmployee with ID {employee_id} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Employee: {e}")

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
        print_employees(cursor)
    elif selection == 2:
        modify_employee(cnx, cursor)
    elif selection == 3:
        create_employee(cnx, cursor)
    elif selection == 4:
        delete_employee(cnx, cursor)
    elif (selection == 5):
        print("\nReturning to main menu...")
        return False
    else:
        print("\nIncorrect input!")
        
    return True

def manage_employees(cnx, cursor):
    """
    Full menu and commands for managing employees (admin command)

    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing

    """
    
    while True:
        print("\nEmployee Management MENU:")
        print("1) Print Employees")
        print("2) Modify Employee")
        print("3) Create Employee")
        print("4) Delete Employee")
        print("5) Return to Main Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            if not select(selection, cnx, cursor):
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        