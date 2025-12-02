from mysql.connector import Error

def print_quality_tests(cursor):
    """
    Lists all quality tests
    
    Takes one parameter:
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    try:
        cursor.execute("SELECT test_ID, sample_time, result_status, comments, batch_ID, performed_by FROM Quality_Test")
        rows = cursor.fetchall()
        print("\nListing all Quality Tests...")
        for row in rows:
            print(f"\nTest ID: {row[0]}, Batch ID: {row[4]}, Performed By (Employee ID): {row[5]}")
            print(f"Result Status: {row[2]}, Sample Time: {row[1]}")
            print(f"Comments: {row[3]}")
    
    except Error as e:
        print(f"Error listing Quality Tests: {e}")
        
def modify_quality_test(cnx, cursor, perms):
    """
    Modify a quality test
    
    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        
    Returns nothing
    """
    #Get the test ID
    test_id = input("\nEnter the Quality Test ID to modify: ").strip()
    if not test_id.isdigit():
        print("Invalid Test ID!\n")
        return
    
    print("\nIf you don't wish to update an attribute, leave it blank.")
    
    new_sample_time = input("\nEnter new Sample Time (YYYY-MM-DD HH:MM:SS): ").strip()
    new_status = input("\nEnter new Status (Pass/Fail/Pending): ").strip()
    new_comments = input("\nEnter new Comments: ").strip()
    
    #only admins can change the employee assigned
    if (perms == 1):
        new_performed_by = input("\nEnter new ID of the Employee performing the test: ").strip()
    else:
        new_performed_by = ""   #will test false
    
    #Building query
    sets = []
    vals = []
    
    if new_sample_time:
        sets.append("sample_time = %s")
        vals.append(new_sample_time)
    
    if new_status:
        sets.append("result_status = %s")
        vals.append(new_status)
        
    if new_comments:
        sets.append("comments = %s")
        vals.append(new_comments)
        
    if new_performed_by:
        sets.append("performed_by = %s")
        vals.append(new_performed_by)
        
    vals.append(test_id)    #append test ID for the WHERE clause
    set_clause = ", ".join(sets)      #join all the set clauses together
        
    query = f"UPDATE Quality_Test SET {set_clause} WHERE test_ID = %s"
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print(f"\nQuality Test with ID {test_id} updated successfully!")
    except Error as e:
        print(f"\nError updating Quality Test: {e}")
        
def create_quality_test(cnx, cursor):
    """
    Create a quality test
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """

    print("\nCreating a new Quality Test...")
    
    batch_id = input("\nEnter the Batch ID that's being tested: ").strip()
    sample_time = input("\nEnter the Sample Time (YYYY-MM-DD HH:MM:SS): ").strip()
    status = input("\nEnter the Status (Pass/Fail/Pending): ").strip()
    comments = input("\nEnter any Comments: ").strip()
    performed_by = input("\nEnter the ID of the Employee performing the test: ").strip()
    
    #Building query using vals array
    vals = []
    
    vals.append(sample_time)
    vals.append(status)
    vals.append(comments)
    vals.append(batch_id)
    vals.append(performed_by)
        
    query = """INSERT INTO Quality_Test
    (sample_time, result_status, comments, batch_ID, performed_by) VALUES
    (%s, %s, %s, %s, %s);"""
    
    try:
        cursor.execute(query, vals)
        cnx.commit()
        print("\nQuality Test created successfully!")
    except Error as e:
        print(f"\nError creating Quality Test: {e}")
        
def delete_quality_test(cnx, cursor):
    """
    Delete a quality test
    
    Takes 2 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        
    Returns nothing
    """
    #Get the test ID
    test_id = input("\nEnter the Quality Test ID to delete: ").strip()
    
    query = "DELETE FROM Quality_Test WHERE test_ID = %s;"
    
    try:
        cursor.execute(query, (test_id,))
        cnx.commit()
        if cursor.rowcount == 0:    #When 0 rows were updated
            print(f"\nNo Quality Test found with ID {test_id}!")
        else:
            print(f"\nQuality Test with ID {test_id} deleted successfully!")
    except Exception as e:
        print(f"\nError deleting Quality Test: {e}")

def select(selection, cnx, cursor, perms):
    """
    Selects and performs a menu command.
    
    Takes 5 parameters:
        selection : int - integer corresponding to chosen command
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 if admin permissions, 0 if not
        
    Returns false if leaving current management menu
    """
    
    if selection == 1:
        print_quality_tests(cursor)
    elif selection == 2:
        modify_quality_test(cnx, cursor, perms)
    elif selection == 3:
        if (perms == 0):    #Return-to-menu command for user level permissions
            print("\nReturning to main menu...")
            return False
        create_quality_test(cnx, cursor)
    elif selection == 4 and perms == 1:     
        delete_quality_test(cnx, cursor)
    elif (selection == 5 and perms == 1):
        print("\nReturning to main menu...")
        return False
    else:
        print("\nIncorrect input!")
        
    return True

def manage_quality_tests(cnx, cursor, perms):
    """
    Full menu and commands for managing quality tests

    Takes 3 parameters:
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
        perms : int - 1 for admin permissions, 0 for user-level permissions
        
    Returns nothing

    """
    
    while True:
        print("\nQuality Test Management MENU:")
        print("1) Print Quality Tests")
        print("2) Modify Quality Test")
        if (perms == 0):
            print("3) Return to Main Menu")
        else:
            print("3) Create Quality Test")
            print("4) Delete Quality Test")
            print("5) Return to Main Menu")
        
        try:
            selection = int(input("\nEnter a command number: "))
            if not select(selection, cnx, cursor, perms):
                break
        except ValueError:
            print("\nIncorrect Input!")
        
        