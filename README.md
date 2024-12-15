# Password Analyzer

## Description
The Password Analyzer is a comprehensive tool designed to evaluate and enhance password security. It helps users analyze the strength of their passwords, provides suggestions for improvement, and allows for secure storage of passwords in a database. 

## Features
- Analyze password strength based on length, character diversity, and common password lists.
- Generate strengthened passwords.
- Encrypt and store passwords securely in a database.
- Manage saved passwords (view, lookup, delete).

## Installation
1. **Create a Database Instance:**
   - Set up a database instance either locally or on the cloud.

2. **Run the SQL Script:**
   - Execute the `database_creation_script.sql` file to create the necessary tables in the database.

3. **Update the Connection String:**
   - Open `analyzer.py` and update the `connection_string` variable with your database credentials.

4. **Install Dependencies:**
   - Install the required Python packages:
     ```bash
     pip install pyodbc bcrypt cryptography
     ```

5. **Generate the Key File:**
   - Run the `key_generator.py` script to generate an encryption key:
     ```bash
     python key_generator.py
     ```

6. **Run the Analyzer:**
   - Execute `analyzer.py` to start the application:
     ```bash
     python analyzer.py
     ```

## Usage
- Launch the application and follow the on-screen prompts to:
  1. Log in or sign up as a user.
  2. Analyze or strengthen and save passwords.
  3. Manage stored passwords (view, lookup, or delete).

## Technologies Used
- **Programming Language:** Python
- **Libraries:**
  - `os` for terminal operations
  - `pyodbc` for database interaction
  - `bcrypt` for hashing passwords
  - `cryptography` for encrypting passwords
  - `random` and `string` for password generation

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the contributors of the `pyodbc`, `bcrypt`, and `cryptography` libraries for enabling secure password handling.

## Contact
For questions or support, contact:
- **Name:** Ben Reinecke
- **Email:** breinecke2@huskers.unl.edu
- **GitHub:** [benreinecke](https://github.com/benreinecke)

