# How to Use
The main.py file contains everything for the application. On its initial execution it will create a database file in the main.py file's directory where it will store the usernames, passwords and notes aswell as the currentuser for the application. These files can not be in seperate directories. You can run the file directly or put it in a folder and create a shortcut and move either the folder or the shortcut anywhere you would like and it will run fine; If you want to do that just right click the main.py and click shortcut and you will be good.

# Requirement
Python installed on system. No need to worry about tkinter it comes with the python install.

# Code
How the program works is all written down in the file to help understanding what is going on easier. Here is a quick over view of the program's layout. Read the comments to get a better understanding in the main.py file.

- **Create Database** - The starting code makes the database file and creates tables or connects to the file if it already exist using sqlite.

- **Pages** - The GUI class is used to travel in between pages and is called the controller for each page and every class after that is it's own page with it's own functions. Each page first has the functions for that page listed on top and the visual UI section right below that. The only page that doesn't have its own distinct functions is the Start Page. The Note and NoteCreation page are related to each other so they interact with what is displayed on one another making frames be attributes to the class.

- **Support Functions** - the support functions are what make any action on that page possible. They remove errors that might of popped up if a user input something wrong or can save and delete notes with a press of a button.

## Note
Users are not required to have passwords

