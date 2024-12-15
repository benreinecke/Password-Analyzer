import os
import string
import random
import pyodbc
import bcrypt
from cryptography.fernet import Fernet

connection_string = (
    # Insert your database connection string here.
)

specialCharacters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ';', ':', '"', "'",
'<', '>', ',', '.', '/', '?', '\\', '|', '`', '~']

# Clear the terminal.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Load in a wordlist.
def loadWordlist(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return set(line.strip().lower() for line in file)

# Hash a password.
def hashPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return hashed

# Load the encryption key
def loadKey():
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()

# Encrypt a stronger password
def encryptPassword(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode('utf-8'))

# Decrypt a stronger password
def decryptPassword(encryptedPassword, key):
    fernet = Fernet(key)
    return fernet.decrypt(encryptedPassword).decode('utf-8')

# Print a detailed analysis of a given password. A password's strength score is determined by the presence of:
#   Long length (12+ characters)
#   Extra long length (16+ characters)
#   Lower-case characters
#   Upper-case characters
#   Numbers
#   Special characters
#   Password does not appear in a list of the most common passwords and phrases
def analyze(password, commonPasswords, mostCommonPasswords):
    score = 0
    long, extraLong, lower, upper, number, special, common, uncommon = False, False, False, False, False, False, False, False
    positiveAttributes, negativeAttributes = "", ""

    # Check the length.
    if len(password) >= 16: extraLong = True
    if len(password) >= 12: long = True

    # Check each character.
    for character in password:
        if character.islower(): lower = True
        elif character.isupper(): upper = True
        elif character.isnumeric(): number = True
        elif character in specialCharacters: special = True
        else:
            print("Your password contains invalid characters!")
            break

    # Check against common passwords.
    if password.lower() not in commonPasswords:
        uncommon = True
    if password.lower() in mostCommonPasswords:
        common = True
  
    # Update the score and attributes
    if long:
        score += 1
        positiveAttributes += "- Long length (12+ characters)\n"
    else:
        negativeAttributes += "- Shorter than 12 characters\n"

    if extraLong:
        score += 1
        positiveAttributes += "- Very long length (16+ characters)\n"
    else:
        negativeAttributes += "- Shorter than 16 characters\n"

    if lower:
        score += 1
        positiveAttributes += "- Lowercase letter(s)\n"
    else:
        negativeAttributes += "- Does not contain lowercase letters\n"

    if upper:
        score += 1
        positiveAttributes += "- Uppercase letter(s)\n"
    else:
        negativeAttributes += "- Does not contain uppercase letters\n"

    if number:
        score += 1
        positiveAttributes += "- Number(s)\n"
    else:
        negativeAttributes += "- Does not contain numbers\n"

    if special:
        score += 1
        positiveAttributes += "- Special character(s)\n"
    else:
        negativeAttributes += "- Does not contain special characters\n"

    if uncommon:
        score += 1
        positiveAttributes += "- Does not contain common words/phrases\n"
    else:
        negativeAttributes += "- Contains common words/phrases\n"

    if common:
        score = 0
        negativeAttributes += "- *CRITICAL* Your password contains one of the 1000 most common words/phrases\n"

    print("Strength score: " + str(score) + "/7\n")
    print("What makes your password strong:\n" + positiveAttributes)
    print("What makes your password weak:\n" + negativeAttributes)

# Return a strengthened password generated from the given password. Show the analysis for both passwords.
# The user can then save the pair of passwords to the database.
def strengthen(password):
    # Ensure password is at least the minimum length
    while len(password) < 32:
        # Select a random element of each type of character.
        randomLowerCharacter = random.choice(string.ascii_lowercase)
        randomUpperCharacter = random.choice(string.ascii_uppercase)
        randomSpecialCharacter = random.choice(''.join(specialCharacters))
        randomNumber = random.randint(0, 9)

        # Append the characters and randomize their order.
        insertString = randomLowerCharacter + randomUpperCharacter + randomSpecialCharacter + str(randomNumber)
        insertString = ''.join(random.sample(insertString, len(insertString)))

        # Insert the random string at a random position in the password.
        insertPosition = random.randint(0, len(password))
        password = password[:insertPosition] + insertString + password[insertPosition:]
    return password

### --- Database Functions --- ###
# Check whether the given password matches the stored password for the given user.
def checkPassword(cursor, username, password):
    query = "SELECT password FROM [User] WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        if bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            # Password matches!
            return True
    # Incorrect username or password.
    return False

# Returns true if the given username is taken (appears in the User table), false otherwise.
def isTaken(cursor, username):
    query = "SELECT 1 FROM [User] WHERE Username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    return result

# Gets the user ID corresponding to the given username of an authenticated user.
def getUserID(cursor, username):
    query = "SELECT userID FROM [User] WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    return int(result[0])

# Insert a new user record given a unique username and password.
def insertUser(cursor, username, password):
    query = "INSERT INTO [User] (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, hashPassword(password),))
    connection.commit()

# Authenticate an existing or add a new user, returning the userID of the user.
def authenticate(cursor):
    clear()
    while True:
        operation = input("Welcome to Password Analyzer!\n1: Log in\n2: Sign up\n3: Exit\n")
        if operation.isnumeric() and int(operation) == 1:
            # Log in.
            clear()
            while True:
                print("---Log in---")
                username = input("Username: ")
                password = input("Password: ")
                # Check that the given password matches.
                if checkPassword(cursor, username, password):
                    break
                else:
                    clear()
                    print("Incorrect username or password.")
            sessionUserID = getUserID(cursor, username)
            return sessionUserID
        elif operation.isnumeric() and int(operation) == 2:
            # Sign up.
            clear()
            while True:
                print("---Sign up---")
                username = input("Username: ")
                password = input("Password: ")
                # Check if the username is already taken.
                if isTaken(cursor, username):
                    clear()
                    print("That username is already taken.")
                else:
                    break
            insertUser(cursor, username, password)
            sessionUserID = getUserID(cursor, username)
            return sessionUserID
        elif operation.isnumeric() and int(operation) == 3:
            clear()
            exit()
        else:
            clear()
            print("Please enter the number next to the operation you would like to perform.")

# Saves the given password and its strengthened version under the User's account.
# Returns true on success, returns false if the old password already exists in the account.
def savePassword(cursor, sessionUserID, oldPassword, strongPassword):
    # Check if this password already exists under this user.
    key = loadKey()
    query = "SELECT oldPassword FROM Password WHERE userID = ?"
    cursor.execute(query, (sessionUserID,))
    passwords = cursor.fetchall()
    for record in passwords:
        if decryptPassword(record[0], key) == oldPassword:
            return False
    # If the oldPassword is unique, save it with its strengthened version.
    query = "INSERT INTO Password (oldPassword, newPassword, userID) VALUES (?, ?, ?)"
    cursor.execute(query, (encryptPassword(oldPassword, key), encryptPassword(strongPassword, key), sessionUserID))
    connection.commit()
    return True

# Returns a list of password pairs that match the given userID.
def getAllPasswords(cursor, sessionUserID):
    key = loadKey()
    # Get all password pairs from the database.
    query = "SELECT oldPassword, newPassword, passwordID FROM Password WHERE userID = ?"
    cursor.execute(query, (sessionUserID,))
    rows = cursor.fetchall()
    # Convert the results into a list of dictionaries with decrypted passwords.
    passwordList = []
    for row in rows:
        passwordList.append({
            "oldPassword": decryptPassword(row[0], key),
            "newPassword": decryptPassword(row[1], key),
            "passwordID": row[2]
        })
    return passwordList

# Returns the password pair corresponding with the given password, if it exists.
def lookupPassword(cursor, sessionUserID, password):
    key = loadKey()
    # Get the list of all password pairs for this user.
    passwordList = getAllPasswords(cursor, sessionUserID)
    # Search for the given password in this list.
    for element in passwordList:
        if element['oldPassword'] == password:
            return element
    return None

# Returns true if the given password is deleted, false otherwise.
def deletePassword(cursor, sessionUserID, password):
    key = loadKey()
    # Get the list of all password pairs for this user.
    passwordList = getAllPasswords(cursor, sessionUserID)
    # Delete the password from the database if it exists.
    for element in passwordList:
        if element['oldPassword'] == password:
            query = "DELETE FROM Password WHERE passwordID = ?"
            cursor.execute(query, (element['passwordID'],))
            connection.commit()
            return True
    return False

### --- Main --- ###
# Connect to the database.
try:
    # Establish connection.
    connection = pyodbc.connect(connection_string)
    # Create a cursor object.
    cursor = connection.cursor()
    # Authenticate the user.
    sessionUserID = authenticate(cursor)
    # Load the common password wordlists.
    commonPasswords = loadWordlist('common_passwords.txt')
    mostCommonPasswords = loadWordlist('most_common_passwords.txt')
    # Work with the database.
    clear()
    while True:
        # Get user input to detrmine the operation.
        operation = input("Please choose an operation below:\n1: Analyze a password\n2: Strengthen a password\n3: Manage my passwords\n4: Exit\n")

        # Perform the operation.
        if operation.isnumeric() and int(operation) == 1:
            # Analyze password.
            clear()
            password = input("Please enter the password you want to analyze: ")
            analyze(password, commonPasswords, mostCommonPasswords)

        elif operation.isnumeric() and int(operation) == 2:
            # Strengthen password.
            clear()
            password = input("Please enter the password you want to strengthen: ")
            # Print the analysis of the old password.
            print("Your password: " + password)
            analyze(password, commonPasswords, mostCommonPasswords)
            # Strengthen the old password.
            strongPassword = strengthen(password)
            # Print the analysis of the strengthened password.
            print("Strong password: " + strongPassword)
            analyze(strongPassword, commonPasswords, mostCommonPasswords)
            # Ask if the user wants to save this password pair to their passwords.
            while True:
                action = input("Would you like to save this password pair to your passwords?\n 1: Yes\n 2: No\n")
                if action.isnumeric() and int(action) == 1:
                    # If not in database, save.
                    if savePassword(cursor, sessionUserID, password, strongPassword):
                        clear()
                        print("This password pair has been saved to your passwords.")
                        break
                    else:
                        clear()
                        print("Your entered password, '" + password + "', has already been strengthened and saved.")
                        print("If you would like to view your saved passwords, please select the 'Manage my passwords' option.")
                        break
                elif action.isnumeric() and int(action) == 2:
                    # Do not save.
                    clear()
                    break
                else:
                    # Invalid input.
                    clear()
                    print("Please enter the number next to the operation you would like to perform.")

        elif operation.isnumeric() and int(operation) == 3:
            # Manage passwords.
            clear()
            while True:
                print("Password Manager")
                action = input("1. View all passwords\n2. Look up a password\n3. Delete a password\n4. Exit\n")
                if action.isnumeric() and int(action) == 1:
                    # View all passwords.
                    clear()
                    passwordList = getAllPasswords(cursor, sessionUserID)
                    # Print all password pairs.
                    count = 1
                    for element in passwordList:
                        print("Password #" + str(count))
                        print("Your password:\t\t" + element['oldPassword'])
                        print("Strong password:\t" + element['newPassword'] + "\n")
                        count += 1
                    break
                elif action.isnumeric() and int(action) == 2:
                    # Look up password.
                    clear()
                    while True:
                        password = input("Enter the password you want to look up: ")
                        passwordPair = lookupPassword(cursor, sessionUserID, password)
                        if passwordPair is not None:
                            clear()
                            print("Your password:\t\t" + passwordPair['oldPassword'])
                            print("Strong password:\t" + passwordPair['newPassword'] + "\n")
                            break
                        else:
                            clear()
                            print("'" + password + "' is not in your passwords.")
                    break
                elif action.isnumeric() and int(action) == 3:
                    # Delete password.
                    clear()
                    while True:
                        password = input("Enter the password you want to delete: ")
                        if deletePassword(cursor, sessionUserID, password):
                            clear()
                            print("Your password, '" + password + "', was successfully deleted.")
                            break
                        else:
                            clear()
                            print("'" + password + "' is not in your passwords.")
                    break
                elif action.isnumeric() and int(action) == 4:
                    clear()
                    exit()
                else:
                    # Invalid input.
                    clear()
                    print("Please enter the number next to the operation you would like to perform.")

        elif operation.isnumeric() and int(operation) == 4:
            clear()
            exit()

        else:
            # Invalid input.
            clear()
            print("Please enter the number next to the operation you would like to perform.")
            continue

        # Ask if the user wants to perform additional operations.
        while True:
            action = input("Would you like to perform another operation?\n1: Yes\n2: No (exit)\n")
            if action.isnumeric() and int(action) == 1:
                # Continue.
                clear()
                break
            elif action.isnumeric() and int(action) == 2:
                clear()
                exit()
            else:
                # Invalid input.
                clear()
                print("Please enter the number next to the operation you would like to perform.")
    
# Catch if unable to connect.
except pyodbc.Error as e:
    print("Error connecting to database:", e)

# Close the connection.
finally:
    if 'connection' in locals() and connection:
        connection.close()

clear()