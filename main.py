import os
import tkinter as tk
from tkinter import ttk

#lists that will be used through out the application
emessage = []
users = []
passwords = []
repasswords = []
currentuser = []

#creating directories for the project
# Starting off by getting this files directory that it is in
PATH = os.path.dirname(__file__)

# Making the Users folder if it doesn't exist
if not os.path.isdir(PATH + '\\Users'):
	os.mkdir(PATH + '\\Users')
	UsersPATH = PATH + '\\Users'
else:
	UsersPATH = PATH + '\\Users'

# making the file that all the usernames and passwords will be stored
if not os.path.isfile(PATH + '\\allusers.txt'):
	file_users = open(PATH + '\\allusers.txt', 'w')
	# The has_users var is will impact how Create will input them into allusers.txt
	has_users = False
	file_users.close()

else:
	with open(PATH + '\\allusers.txt', 'r') as file_users:
		file_users = file_users.read()
		if file_users:
			has_users = True
			# This .split is why has_users var is nessecary
			# the first user written in can't have a ',' behind.
			# while every user that isn't first would need it.
			userlist = file_users.split(',')

			# seperating the usernames and passwords in the file
			for i in range(len(userlist)):
				if i%2 == 0:
					users.append(userlist[i])

				else:
					passwords.append(userlist[i])
		
		else:
			has_users = False

# Making the currentuser file
if not os.path.isfile( PATH + '\\currentuser.txt'):
    currentuser = open( PATH + '\\currentuser.txt', 'w')
    currentuser.close()

# if it exist it will immediately log that user in
else:
	with open(PATH + '\\currentuser.txt', 'r') as cu:
		currentuser.append(cu.read())

	# see if currentuser.txt is empty
	if not users.__contains__(currentuser[0]):
		currentuser.pop()
	else:
		currentuserPATH = UsersPATH + '\\{cu}'.format(cu = currentuser[0])

# get all the files in the current users path
def retreive_all_CurrentUser_files():
	for i in os.listdir(currentuserPATH):
		i = i[:-4]
		# you will see note 
		Note.Notes_List.insert(tk.END,i)

# change currentuserPATH
def change_currentpath(user):
	global currentuserPATH
	with open(PATH + '\\currentuser.txt', 'w') as cu:
		cu.write(user)

	if currentuser:
		currentuser.pop()
		currentuser.append(user)
	else:
		currentuser.append(user)

	currentuserPATH = UsersPATH + f'\\{user}'

#Every class is its own page accept the GUI class.
#This class is what is used to navigate in between other pages. 

class GUI(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)

		GUI.ins = self

		self.geometry('850x500')
		self.minsize(850,500)

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_columnconfigure(0, weight = 1)
		container.grid_rowconfigure(0, weight = 1)
		
		self.frames = {}

		for F in (Start, Create, SignIn, Note, NoteCreation):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")

		if currentuser:
			retreive_all_CurrentUser_files()
			self.show_frame(Note)
		else:
			self.show_frame(Start)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


class Start(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# what is used for the GUI for this page

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		Label = ttk.Label(Master_Frame, text='Would you like to create a account or log in?', font='calibri 10 bold', anchor='n')
		Label.pack(fill='x', pady=9)

		Create_Button = ttk.Button(Master_Frame, text='Create', command=lambda:controller.show_frame(Create))
		Create_Button.pack(side='left',fill='x',expand=1,padx=3)

		SignIn_Button = ttk.Button(Master_Frame, text='Log In', command=lambda:controller.show_frame(SignIn))
		SignIn_Button.pack(side='right', fill='x',expand=1,padx=3)

# This is for removing the errors that might pop up if a user inputs something incorrectly in the Create,signin,Note, and notecreation pages
def remove_error():
	if emessage:
		emessage[0].pack_forget()
		emessage.pop()

# Create page
class Create(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# the variables for the entryboxes
		user = tk.StringVar()
		password = tk.StringVar()
		repassword = tk.StringVar()

		# Functions

		# back button func
		def clear():
			remove_error()
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0, tk.END)
			RePassword_entry.delete(0, tk.END)
			controller.show_frame(Start)

		#checks to make sure the username in the username entry box does not exist already and makes sure it is a acceptable length and
		#gives errors if it does have something wrong with it
		def checkusername():
			# username too long
			if len(Username_entry.get()) > 15:
				remove_error()
				Username_entry.delete(0,tk.END)
				username_long = ttk.Label(Error_Frame, text='username is too long >15', font='calibri 10 bold', foreground='red')
				username_long.pack()
				emessage.append(username_long)
				# boolean value
				return 0
			# Username too short
			if Username_entry.get() == '' or len(Username_entry.get()) < 5:
				remove_error()
				Username_entry.delete(0,tk.END)
				username_short = ttk.Label(Error_Frame, text='username is too short <5', font='calibri 10 bold', foreground='red')
				username_short.pack()
				emessage.append(username_short)
				return 0

			# username already exist or username field is empty
			if users.__contains__(Username_entry.get()) and Username_entry != '':
				remove_error()
				Username_entry.delete(0,tk.END)
				username_exist = ttk.Label(Error_Frame, text='username exist', font='calibri 10 bold', foreground='red')
				username_exist.pack()
				emessage.append(username_exist)
				return 0
			# boolean for the if statement this func will be called in
			return 1

		#functions to be bind to key strokes for the entry boxes

		# for the Username entry
		def passfocus(event):
			if checkusername():
				Password_entry.focus()

		# for the password entry
		def repassfocus(event):
			if checkusername():
				RePassword_entry.focus()

		# for the repass entry
		def create_account(event):
			if RePassword_entry.get() == Password_entry.get() and checkusername():
				users.append(Username_entry.get())
				passwords.append(Password_entry.get())

				os.mkdir(UsersPATH + '\\{user}'.format(user = Username_entry.get()))

				change_currentpath(Username_entry.get())
				
				if has_users:
					with open('allusers.txt', 'a') as userf:
						userf.write(',' + Username_entry.get() + ',' + Password_entry.get())
				else:
					with open('allusers.txt', 'a') as userf:
						userf.write(Username_entry.get() + ',' + Password_entry.get())

				

				controller.show_frame(Note)

				remove_error()
				Username_entry.delete(0, tk.END)
				Password_entry.delete(0, tk.END)
				RePassword_entry.delete(0, tk.END)
			
			else:
				remove_error()
				Username_entry.delete(0, tk.END)
				Password_entry.delete(0, tk.END)
				RePassword_entry.delete(0, tk.END)
				password_matching_error = ttk.Label(Error_Frame, text='passwords did not match', font='calibri 10 bold', foreground='red')
				password_matching_error.pack()
				emessage.append(password_matching_error)
				Username_entry.focus()

		# Everything on the Create Page

		Back_Button = ttk.Button(self, text='Back', command=clear)
		Back_Button.place(x=10,y=10)

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		Error_Frame = tk.Frame(Master_Frame)
		Error_Frame.pack()

		Username_Frame = tk.Frame(Master_Frame)
		Username_Frame.pack(pady=3)

		Username_Label = ttk.Label(Username_Frame, text='enter username:', font='calibri 10 bold')
		Username_Label.pack(anchor='w')

		Username_entry = ttk.Entry(Username_Frame, textvariable=user, width=30)
		Username_entry.pack()
		Username_entry.bind('<Return>', passfocus)

		Password_Frame = tk.Frame(Master_Frame)
		Password_Frame.pack(pady=3)

		Password_Label = ttk.Label(Password_Frame, text='enter password:', font='calibri 10 bold')
		Password_Label.pack(anchor='w')

		Password_entry = ttk.Entry(Password_Frame, textvariable=password, width=30, show='*')
		Password_entry.pack()
		Password_entry.bind('<Return>', repassfocus)

		RePassword_Frame = tk.Frame(Master_Frame)
		RePassword_Frame.pack()

		RePassword_Label = ttk.Label(RePassword_Frame, text='renter password:', font='calibri 10 bold')
		RePassword_Label.pack(anchor='w')

		RePassword_entry = ttk.Entry(RePassword_Frame, textvariable=repassword, width=30, show='*')
		RePassword_entry.pack()
		RePassword_entry.bind('<Return>', create_account)


# Sign in page
class SignIn(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#entry box variables

		user = tk.StringVar()
		password = tk.StringVar()

		# functions

		def clear():
			remove_error()
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0, tk.END)
			controller.show_frame(Start)

		# focuses on the password entry box and is tied to the username entry box
		def passfocus(event):
			Password_entry.focus()

		# called with the pass entry box
		def signing_in(event):
			remove_error()
			# See if the username maches the password
			if users.__contains__(Username_entry.get()) and passwords.__contains__(Password_entry.get()):
				if users.index(Username_entry.get()) == passwords.index(Password_entry.get()):
					# change path and get files
					change_currentpath(Username_entry.get())
					retreive_all_CurrentUser_files()
					# go to Note Page
					controller.show_frame(Note)
					# clear everything on this page
					remove_error()
					Username_entry.delete(0, tk.END)
					Password_entry.delete(0, tk.END)
					return
			
			# give an error if it was wrong
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0,tk.END)
			wronginput = ttk.Label(Error_Frame, text='incorrect username or password', font='calibri 10 bold', foreground='red')
			wronginput.pack()
			emessage.append(wronginput)
			Username_entry.focus()

		#Gui for Sign in

		Back_Button = ttk.Button(self, text='Back', command=clear)
		Back_Button.place(x=10,y=10)

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		Error_Frame = tk.Frame(Master_Frame)
		Error_Frame.pack()

		Username_Frame = tk.Frame(Master_Frame)
		Username_Frame.pack(pady=3)

		Username_Label = ttk.Label(Username_Frame, text='enter username:', font='calibri 10 bold')
		Username_Label.pack(anchor='w')

		Username_entry = ttk.Entry(Username_Frame, textvariable=user, width=30)
		Username_entry.pack()
		Username_entry.bind('<Return>', passfocus)

		Password_Frame = tk.Frame(Master_Frame)
		Password_Frame.pack(pady=3)

		Password_Label = ttk.Label(Password_Frame, text='enter password:', font='calibri 10 bold')
		Password_Label.pack(anchor='w')

		Password_entry = ttk.Entry(Password_Frame, textvariable=password, width=30)
		Password_entry.pack()
		Password_entry.bind('<Return>', signing_in)

# Note Page
class Note(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#what is used for the listbox
		notefiles = []
		notefilesVar = tk.StringVar(value=notefiles)

		# functions

		# get note
		def bring_up_note(event):
			remove_error()
			# Note.selection is what is picked from the group  ///  Note.Notes_list is the box that all the notes' names are in
			Note.selection = [Note.Notes_List.get(i) for i in Note.Notes_List.curselection()][0]
			# Getting note and writing it down in the Note_Contents
			with open(currentuserPATH + '\\{file}.txt'.format(file = Note.selection)) as F:
				all_text = F.read()
				Note_Contents.delete('1.0','end')
				Note_Contents.insert('1.0', all_text)

		# logs out the current user and goes to the start
		def Log_Out():
			remove_error()
			Note.Notes_List.delete(0, tk.END)
			Note_Contents.delete('1.0','end')
			cu = open(PATH + '\\currentuser.txt', 'w')
			cu.close()
			controller.show_frame(Start)

		# make new note and go to the note creation page
		def New_Note():
			remove_error()
			# Note creation is the class before this one more on NoteCreation.Old_name_Frame in that class
			NoteCreation.Old_Name_Frame.pack_forget()
			controller.show_frame(NoteCreation)

		# rename existing note
		def Rename_Note():
			remove_error()
			# if a file from the list is selected
			if Note.Notes_List.curselection():
				
				if NoteCreation.Old_Name_Frame.winfo_ismapped():
					NoteCreation.Old_Name_Frame.pack_forget()
				if NoteCreation.Name_Frame.winfo_ismapped():
					NoteCreation.Name_Frame.pack_forget()

				NoteCreation.Old_Name_Frame.pack()
				NoteCreation.Name_Frame.pack(padx=15, pady=15)
				# set the text on that page to the name of the current note
				NoteCreation.text.set(Note.selection)
				controller.show_frame(NoteCreation)
			else:
				# Error
				nofile = ttk.Label(Error_Frame, text='no file selected, can\'t rename', foreground='red')
				nofile.pack()
				emessage.append(nofile)

		# Save, the quit parameter verys for the save and the save&quit button this def is assigned to
		def Save(quit):
			remove_error()
			if hasattr(Note, 'selection'):
				with open(currentuserPATH + '\\{file}.txt'.format(file = Note.selection), 'w') as F:
					F.write(Note_Contents.get('1.0', tk.END)[:-1])

				if quit == True:
					GUI.destroy(GUI.ins)
			else:
				# Error
				nofile = ttk.Label(Error_Frame, text='no file selected, can\'t save', foreground='red')
				nofile.pack()
				emessage.append(nofile)
			
		# UI for Note Page

		#left frame

		Left_Frame = tk.Frame(self)
		Left_Frame.pack(side='left', fill='y')

		menu_button_frame = tk.Frame(Left_Frame, borderwidth='2', relief='groove')
		menu_button_frame.pack(ipady=5)

		LogOut = ttk.Button(menu_button_frame, text='Log Out', width=15, command=Log_Out)
		LogOut.pack(side='left', padx=4)

		rename_note_button = ttk.Button(menu_button_frame, text='rename note', width= 15, command=Rename_Note)
		rename_note_button.pack(side='left')

		New_Note_Button = ttk.Button(menu_button_frame, text='new note', width=15, command=New_Note)
		New_Note_Button.pack(side='right', padx=4)


		User_Notes = tk.Frame(Left_Frame)
		User_Notes.pack(expand=1, fill='both')

		# Created as an attribute because it will be interacted with in the NoteCreation
		Note.Notes_List = tk.Listbox(User_Notes, listvariable=notefilesVar, font='calibri 11')
		Note.Notes_List.pack(side='left', expand=1, fill='both')
		Note.Notes_List.bind('<<ListboxSelect>>', bring_up_note)

		scrollbar = tk.Scrollbar(User_Notes, orient='vertical', command=Note.Notes_List.yview)
		scrollbar.pack(side='right', fill='y')

		Note.Notes_List['yscrollcommand'] = scrollbar.set

		#right frame

		right_frame = tk.Frame(self)
		right_frame.pack(side='right', fill='both', expand=1)

		Save_Button_frame = tk.Frame(right_frame, borderwidth='2', relief='groove')
		Save_Button_frame.pack(ipady=5, fill='x')

		Error_Frame = tk.Frame(Save_Button_frame)
		Error_Frame.pack(side='left', padx=4)

		SaveAndQuit_Button = ttk.Button(Save_Button_frame, text='Save & Quit', width=11, command=lambda:Save(True))
		SaveAndQuit_Button.pack(side='right', padx=4)

		Save_Button = ttk.Button(Save_Button_frame, text='Save', width=11, command=lambda:Save(False))
		Save_Button.pack(side='right', padx=4)

		Note_Frame = tk.Frame(right_frame)
		Note_Frame.pack(expand=1, fill='both')

		Note_Contents = tk.Text(Note_Frame, wrap='word', font='calibri 12')
		Note_Contents.pack(side='left', expand=1,fill='both')

		scrollbar = tk.Scrollbar(Note_Frame, orient='vertical', command=Note_Contents.yview)
		scrollbar.pack(side='right', fill='y')

		Note_Contents['yscrollcommand'] = scrollbar.set

# Note Creation page
class NoteCreation(tk.Frame):
	def __init__(self,parent, controller):
		tk.Frame.__init__(self, parent)

		def clear():
			remove_error()
			Name_Entry.delete(0, tk.END)
			controller.show_frame(Note)

		# Rename existing note
		def create_note_rename(event):
			remove_error()
			# invalid characters
			badchars = [i for i in Name_Entry.get() if i == '\\' or i =='/' or i == ':' or i == '*' or i =='?' or i =='"' or i =='<' or i =='>' or i == '|']
			if badchars:
				
				Name_Entry.delete(0, tk.END)
				unusablechars = ttk.Label(Error_Frame, text='can\'t use\n\/:*?"<>|', foreground='red')
				unusablechars.pack()
				emessage.append(unusablechars)
				return None

			# nothing Typed
			if Name_Entry.get() == '':
				Name_Entry.delete(0, tk.END)
				nochars = ttk.Label(Error_Frame, text='no charecters typed', foreground='red')
				nochars.pack()
				emessage.append(nochars)
				return None

			# Name is too long
			if len(Name_Entry.get()) > 35:
				Name_Entry.delete(0, tk.END)
				Notetoolong = ttk.Label(Error_Frame, text='too long to be displayed', foreground='red')
				Notetoolong.pack()
				emessage.append(Notetoolong)
				return None

			# Change the old name and put it in the Note.Notes_list in Note
			if NoteCreation.Old_Name_Frame.winfo_ismapped():
				for i in Note.Notes_List.curselection():
					Note.Notes_List.delete(i)
					Note.Notes_List.insert(tk.END, Name_Entry.get())
				os.rename(f'{currentuserPATH}\\{Note.selection}.txt', f'{currentuserPATH}\\{Name_Entry.get()}.txt')
				Note.selection = Name_Entry.get()
				Name_Entry.delete(0, tk.END)
				controller.show_frame(Note)

			# Make note and put it in Note.Notes_List
			else:
				Note.Notes_List.insert(tk.END, Name_Entry.get())
				New_f = open(currentuserPATH + '\\{file}.txt'.format(file = Name_Entry.get()), 'w')
				New_f.close()
				Name_Entry.delete(0, tk.END)
				controller.show_frame(Note)

		# UI for Note creation page
		Back_Button = ttk.Button(self, text='Back', command=clear)
		Back_Button.place(x=10,y=10)

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1)

		Error_Frame = tk.Frame(Master_Frame)
		Error_Frame.pack()

		# NoteCreation.Old_name_Frame is a frams for holding the text thap will be displayed if rename is selected
		# It is also accessed on the Note page too
		NoteCreation.Old_Name_Frame = tk.Frame(Master_Frame)
		NoteCreation.Old_Name_Frame.pack(padx=15, pady=10)

		Old_Label = ttk.Label(NoteCreation.Old_Name_Frame, text='old note\'s name:', font='calibri 10  bold underline')
		Old_Label.pack()

		# text to go on the .Old_name Frame
		NoteCreation.text = tk.StringVar()
		# Used to change the text of the .text attribute
		NoteCreation.text.set('')
		NoteCreation.Old_file_name = ttk.Label(NoteCreation.Old_Name_Frame, textvariable=NoteCreation.text, font='calibri 11')
		NoteCreation.Old_file_name.pack()

		NoteCreation.Name_Frame = tk.Frame(Master_Frame)
		NoteCreation.Name_Frame.pack(padx=15, pady=15)

		Name_Label = ttk.Label(NoteCreation.Name_Frame, text='Name:')
		Name_Label.pack(side='left')

		Name_Entry = ttk.Entry(NoteCreation.Name_Frame, width=40)
		Name_Entry.pack(side='right')
		Name_Entry.bind('<Return>', create_note_rename)

app = GUI()
app.mainloop()
