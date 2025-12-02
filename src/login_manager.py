import csv

def load_login_info(filepath='../data/users.csv'):
    """
    Takes in optional parameter filepath (default is '../data/users.csv') and reads it.
    Converts data into a logins dictionary of the format:
        {
            username: {'password': '...', 'perms': 0 or 1}  
        }

    """
    logins = {}

    #Open file for read permissions
    with open(filepath, "r", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')    #file is tab-delimited
        next(spamreader)    #skip first line (header)
        
        for row in spamreader:
            #Construct logins dictionary
            logins[row[0]] = {'password': row[1], 'perms': int(row[2])}
            
    return logins

def check_login(username, password, logins):
    """
    Checks if there is a successful login with a provided username/password
    
    Takes in three parameters:
        username : string - username to attempt login with
        password : string - password to attempt login with
        logins : dictionary - login information to check username and password with
        
    Returns:
        boolean - True if successful login, False if not
        int - 1 if user has admin permissions, 0 if not

    """
    user = logins.get(username)
    if not user:
        print("User doesn't exist!\n")
        return False, None
    if user['password'] != password:
        print("Incorrect password!\n")
        return False, None
    print(f"Logged in as: {username}")
    return True, user['perms']



    
        