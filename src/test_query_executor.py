from mysql.connector import Error

def execute_test_queries(filepath, cnx, cursor):
    """
    Reads the MySQL file at the given filepath and executes one command at a time;
    There are specialized outputs following each command to print its results.
    
    Takes two parameters:
        filepath : string - string of the filepath to the .sql file
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
    
    Returns nothing:
    """
    print("\nExecuting Test Queries...")
    print("Press Enter to Run each Query")
    
    statements = None
    user_prompts = ("\nTest 1: Select the names and IDs of all Employees who've been assigned a Quality Test, and how many tests they've been assigned: ",
                    "\nTest 2: Select the names, units, and IDs of all Products and the Total Quantity ordered for each: ",
                    "\nTest 3: Select the names, units, and IDs of all Raw Materials and the Total Quantity used in Batch Consumptions",
                    "\nTest 4: Select the names, locations, and IDs of all Plants and their total production quantity from completed Batches",
                    "\nTest 5: Select the names, industries, and IDs of all Customers along with their total Order count and value")
    display_names = (("Employee ID", "Name", "Tests Assigned"), ("Product ID","Name","Total Quantity Ordered","Unit"), ("Material ID","Name","Total Quantity Used","Unit"), ("Plant ID","Name","Location","Total Production Quantity"), ("Customer ID","Name","Industry","Total Order Count","Total Order Value"))
    
    
    with open(filepath, "r") as file:
        statements = file.read().split(";")
        
    i = 0
    for statement in statements:
        if not statement.strip():
            continue
        
        input(user_prompts[i])
        
        new_statement = ""
        
        for line in statement.split("\n"):
            line_strip = line.strip()
            if line_strip and not line_strip.startswith("--"):   #Remove comments
                new_statement += line_strip + " "
                
        query = new_statement.strip()
        if not query:   #error: empty query
            i += 1
            continue
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            print_query_result(display_names[i], rows)
        
        except Error as e:
            print(f"\nError printing results: {e}")
            input("Press Enter to continue: ")
            
        i += 1
        
    print ("\nAll test queries executed, returning to Main Menu...")
        
    
def print_query_result(display_names, rows):
    print("\nPrinting Query Results...")
    for row in rows:
        print()
        i = 0
        for name in display_names:
            print(f"{name}: {row[i]}")
            i += 1
    input("\nFinished printing, press Enter to continue: ")
        