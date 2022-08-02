# How to Use
The main.py file contains everything for the application. On execution it will create additional files for where the users and the user's files will be stored. The program is ment to be ran in its own folder, it will create 2 .txt files and 1 folder in the current directory the file is located in. In that folder you can right click the main.py file and make a shortcut if you don't want to open the folder everytime you use it and have that folder hidden somewhere else.

# Note
When renaming a note do not highlight the bar and drag it pass the far left or the rename function will keep the same name in the application and rename the file itself making it so you can't rename the file a second time until restart. Its a little weird just keep that in mind when using the program.

# Requirement
Python installed on system. tkinter should come with the python install.

# Code
How the program works is all written down in the file to help understanding what is going on easier. Here is a quick over view of the program's layout. Read the comments to get a better understanding.

- **Making Paths** - The starting code you first see is to check if the required files and folder for the program to work are present, and if they are not it will create them.

- **Pages** - The GUI class is used to travel in between pages and is called the controller for each page and is the only class that isn't its own individual page. Each page first has the functions for that page listed on top and the visual UI section right below that. The only page that doesn't have its own distinct functions is the Start Page. The Note and NoteCreation page are related to each other so they interact with what is displayed on each other.

- **Support Functions** - there are tfunctions that are used to change the directory files will be saved in for each user or remove errors that might of popped up if a user input something wrong. The support functions that don't fall into the other 2 catagories are retreive_all_CurrentUser_files, change_currentpath, and remove_error.

