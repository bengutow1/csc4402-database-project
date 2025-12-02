import sys
from mysql.connector import Error

def execute_sql_file(filepath, cnx, cursor):
    """
    Reads the MySQL file at the given filepath and executes all its commands.
    
    Takes two parameters:
        filepath : string - string of the filepath to the .sql file
        cnx : connection object - object that connects MySQL with Python
        cursor: cursor object - object that points to the database, used to execute commands
    
    Returns nothing:
    
    """
    statements = None
    
    try:
        with open(filepath, "r") as file:
            statements = file.read()
        
        for result in cursor.execute(statements, multi=True):
            pass
        
        cnx.commit()  #Commit changes to the database
        print(f"Successfully executed {filepath}\n")
    
    except Error as e:
        print(f"Error executing {filepath}: {e}")
        print("Exiting program...")
        sys.exit()
        