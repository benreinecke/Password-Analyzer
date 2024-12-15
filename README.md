Password Analyzer

Description

The Password Analyzer is a comprehensive tool designed to evaluate and enhance password security. It helps users analyze the strength of their passwords, provides suggestions for improvement, and allows for secure storage of passwords in a database.

Features

Analyze password strength based on length, character diversity, and common password lists.

Generate strengthened passwords.

Encrypt and store passwords securely in a database.

Manage saved passwords (view, lookup, delete).

Installation

Create a Database Instance:

Set up a database instance either locally or on the cloud.

Run the SQL Script:

Execute the database_creation_script.sql file to create the necessary tables in the database.

Update the Connection String:

Open analyzer.py and update the connection_string variable with your database credentials.

Install Dependencies:

Install the required Python packages:

pip install pyodbc bcrypt cryptography

Generate the Key File:

Run the key_generator.py script to generate an encryption key:

python key_generator.py

Run the Analyzer:

Execute analyzer.py to start the application:

python analyzer.py

Usage

Launch the application and follow the on-screen prompts to:

Log in or sign up as a user.

Analyze or strengthen passwords.

Manage stored passwords (view, lookup, or delete).

Configuration

Connection String: Update the connection_string in analyzer.py with your database credentials.

Common Password Lists: Ensure the common_passwords.txt and most_common_passwords.txt files are available in the project directory.

Technologies Used

Programming Language: Python

Libraries:

os for terminal operations

pyodbc for database interaction

bcrypt for hashing passwords

cryptography for encrypting passwords

random and string for password generation

Example Usage

Analyze a Password

Please enter the password you want to analyze: examplePassword
Strength score: 5/7
What makes your password strong:
- Lowercase letter(s)
- Uppercase letter(s)
- Number(s)
- Special character(s)
- Long length (12+ characters)
What makes your password weak:
- Shorter than 16 characters

Strengthen a Password

Please enter the password you want to strengthen: example
Your strengthened password: Exa1@mpl$Pqwe&zx8Rty!
Strength score: 7/7

Contributing

Contributions are welcome! To contribute:

Fork the repository.

Create a new branch:

git checkout -b feature/YourFeature

Commit your changes:

git commit -m 'Add some feature'

Push to the branch:

git push origin feature/YourFeature

Submit a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

Special thanks to the contributors of the pyodbc, bcrypt, and cryptography libraries for enabling secure password handling.

Contact

For questions or support, contact:

Name: Your Name

Email: your.email@example.com

GitHub: yourusername
