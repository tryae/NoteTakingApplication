import sqlite3
import tkinter as tk
from tkinter import ttk

#database
con = sqlite3.connect('users.db')
cur = con.cursor()

# SEE IF ANY TABLE HAVE BEEN MADE
# ONLY NEED TO FETCHONE BECAUSE IF ONE IS CREATED THAN ALL OTHERS WERE
if cur.execute('SELECT name FROM sqlite_master').fetchone():
	# IF  THERE IS A TABLE WE DONT HAVETO DO ANYTHING
	pass

# MAKE THEM IF THEY AREN'T
else:
	cur.execute('CREATE TABLE users(username, password)')
	cur.execute('CREATE TABLE current(username)')
	cur.execute('CREATE TABLE notes(user, name, contents)')

# used for the error frame on the create, signin and note pages
emessage = []

# get all the notes from the current user
def retreive_all_CurrentUser_files():
	if cur.execute('SELECT user from Notes').fetchone():
		for i in cur.execute('SELECT name FROM notes WHERE user = ?', (cur.execute('SELECT username FROM current').fetchone()[0], )):
			Note.Notes_List.insert(tk.END, i[0])

#creating the gui
class GUI(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)

		GUI.ins = self

		self.geometry('1000x500')
		self.minsize(1000,500)

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_columnconfigure(0, weight = 1)
		container.grid_rowconfigure(0, weight = 1)
		
		#makes a dictionary for the individual pages
		self.frames = {}

		for F in (Start, Create, SignIn, Note, NoteCreation):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")

		# Sees if there is a current user
		if cur.execute('SELECT username FROM current').fetchone():
			# gets all the notes of that user
			retreive_all_CurrentUser_files()
			# change the title to the username
			self.title(cur.execute('SELECT username FROM current').fetchone()[0])
			self.show_frame(Note)
		else:
			self.title('Note Application')
			self.show_frame(Start)

	# function used to show each of the different pages
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class Start(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#the Gui for the Start frame which leads to both Create and Signin frames for the application with the create login buttons
		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		Label = ttk.Label(Master_Frame, text='Would you like to create a account or log in?', font='calibri 10 bold', anchor='n')
		Label.pack(fill='x', pady=9)

		Create_Button = ttk.Button(Master_Frame, text='Create', command=lambda:controller.show_frame(Create))
		Create_Button.pack(side='left',fill='x',expand=1,padx=3)

		SignIn_Button = ttk.Button(Master_Frame, text='Log In', command=lambda:controller.show_frame(SignIn))
		SignIn_Button.pack(side='right', fill='x',expand=1,padx=3)

#removes the errors that already exist if there is any for each of the pages
def remove_error():
	if emessage:
		emessage[0].pack_forget()
		emessage.pop()

class Create(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#the variables for the entryboxes
		user = tk.StringVar()
		password = tk.StringVar()
		repassword = tk.StringVar()

		# Functions for the Create Page

		# Repacks the frames so the error frame doesn't stay enlarged after a error is packed to it
		def repack():
			Username_Frame.pack_forget()
			Password_Frame.pack_forget()
			RePassword_Frame.pack_forget()
			Submit_Button.pack_forget()
			Create.Error_Frame.pack_forget()
			Create.Error_Frame = tk.Frame(Master_Frame)
			Create.Error_Frame.pack()
			Username_Frame.pack(pady=3)
			Password_Frame.pack(pady=3)
			RePassword_Frame.pack(pady=3)
			Submit_Button.pack()
	
		# Back removes the current error then repacks and erases the entry boxes
		def back():
			remove_error()
			repack()
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0, tk.END)
			RePassword_entry.delete(0, tk.END)
			controller.show_frame(Start)

		#checks to make sure the username in the username entry box does not exist already and makes sure it is a acceptable length and
		#gives errors if it does have something wrong with it
		# it returns a 1 or 0 for the if statement if the program is used with keybinds in the focus funtions
		def checkusername():
			remove_error()
			# over 15
			if len(Username_entry.get()) > 15:
				Username_entry.delete(0,tk.END)
				username_long = ttk.Label(Create.Error_Frame, text='username is too long', font='calibri 10 bold', foreground='red')
				username_long.pack()
				emessage.append(username_long)
				return 0

			# under 5
			if Username_entry.get() == '' or len(Username_entry.get()) < 5:
				Username_entry.delete(0,tk.END)
				username_short = ttk.Label(Create.Error_Frame, text='username is too short', font='calibri 10 bold', foreground='red')
				username_short.pack()
				emessage.append(username_short)
				return 0

			# does it exist
			if cur.execute('SELECT username FROM users WHERE username = ?', (Username_entry.get(), )).fetchone() and Username_entry.get() != '':
				Username_entry.delete(0,tk.END)
				username_exist = ttk.Label(Create.Error_Frame, text='username exist', font='calibri 10 bold', foreground='red')
				username_exist.pack()
				emessage.append(username_exist)
				return 0

			return 1

		#functions to be bind to key strokes for the entry boxes
		def passfocus(event):
			if checkusername():
				repack()
				Password_entry.focus()

		def repassfocus(event):
			if checkusername():
				repack()
				RePassword_entry.focus()

		# creates the account
		def create_account(event):
			# see if the passwords match and checks the username
			if RePassword_entry.get() == Password_entry.get() and checkusername():
				# put it in the database
				cur.execute('INSERT INTO users VALUES(?, ?)', (Username_entry.get(), Password_entry.get()))
				cur.execute('INSERT INTO current VALUES(?)', (Username_entry.get(),))
				con.commit()

				# change title to username
				controller.title(Username_entry.get())
				# show page
				controller.show_frame(Note)
				# clear the entry boxes
				Username_entry.delete(0, tk.END)
				Password_entry.delete(0, tk.END)
				RePassword_entry.delete(0, tk.END)
			
			else:
				# remove a possible prexisting error and put up its own
				remove_error()
				Username_entry.delete(0, tk.END)
				Password_entry.delete(0, tk.END)
				RePassword_entry.delete(0, tk.END)
				password_matching_error = ttk.Label(Create.Error_Frame, text='passwords did not match', foreground='red')
				password_matching_error.pack()
				emessage.append(password_matching_error)
				Username_entry.focus()
		
		# binding the submit this way makes sure the proper error is displayed
		def submit():
			if checkusername():
				create_account('a')

		#Gui, all the widgets for this page

		Back_Button = ttk.Button(self, text='Back', command=back)
		Back_Button.place(x=10,y=10)

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		Create.Error_Frame = tk.Frame(Master_Frame)
		Create.Error_Frame.pack()

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
		RePassword_Frame.pack(pady=3)

		RePassword_Label = ttk.Label(RePassword_Frame, text='renter password:', font='calibri 10 bold')
		RePassword_Label.pack(anchor='w')

		RePassword_entry = ttk.Entry(RePassword_Frame, textvariable=repassword, width=30, show='*')
		RePassword_entry.pack()
		RePassword_entry.bind('<Return>', create_account)

		Submit_Button = ttk.Button(Master_Frame, text='Submit', command=submit)
		Submit_Button.pack()

class SignIn(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#entry box variables
		user = tk.StringVar()
		password = tk.StringVar()

		#functions

		# repacks the frames so the error frame doesn't stay enlarged after error is packed
		def repack():
			Username_Frame.pack_forget()
			Password_Frame.pack_forget()
			Submit_Button.pack_forget()
			SignIn.Error_Frame.pack_forget()
			SignIn.Error_Frame = tk.Frame(Master_Frame)
			SignIn.Error_Frame.pack()
			Username_Frame.pack(pady=3)
			Password_Frame.pack(pady=3)
			Submit_Button.pack()

		# back clears the error and erases text in the entry boxes
		def back():
			remove_error()
			repack()
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0,tk.END)
			controller.show_frame(Start)

		# keybinded function for focusing on the password entrybox
		def passfocus(event):
			Password_entry.focus()

		def signing_in(event):
			remove_error()
			# sees if that is a username in the database
			if cur.execute('SELECT username FROM users WHERE username = ?', (Username_entry.get(), )).fetchone():
				# sees if the password for that username matches
				if cur.execute('SELECT password FROM users WHERE username = ?', (Username_entry.get(), )).fetchone()[0] == Password_entry.get():
					# put the new current user in
					cur.execute('INSERT INTO current VALUES(?)', (Username_entry.get(),))
					con.commit()

					# change the title to username
					controller.title(Username_entry.get())
					# clear entryboxes
					Username_entry.delete(0, tk.END)
					Password_entry.delete(0, tk.END)

					# get the user's files
					retreive_all_CurrentUser_files()
					controller.show_frame(Note)
					# return so the rest doesn't run if this is successful
					return
			
			# make an error if there is a problem with the username and password
			Username_entry.delete(0, tk.END)
			Password_entry.delete(0,tk.END)
			wronginput = ttk.Label(SignIn.Error_Frame, text='incorrect username or password', font='calibri 10 bold', foreground='red')
			wronginput.pack()
			emessage.append(wronginput)

			Username_entry.focus()

		#Gui for the signin page

		Back_Button = ttk.Button(self, text='Back', command=back)
		Back_Button.place(x=10,y=10)

		Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		Master_Frame.pack(expand=1, ipadx=5, ipady=5)

		SignIn.Error_Frame = tk.Frame(Master_Frame)
		SignIn.Error_Frame.pack()

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

		# the 'a' variable passed in does nothing but the function has a parameter so it's needed
		Submit_Button = ttk.Button(Master_Frame, text='Submit', command=lambda:signing_in('a'))
		Submit_Button.pack()

class Note(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#what is used for the listbox
		notefiles = []
		notefilesVar = tk.StringVar(value=notefiles)

		# bring up Note's contents when it is clicked in the listbox
		def bring_up_note(event):
			remove_error()
			Note.selection = [Note.Notes_List.get(i) for i in Note.Notes_List.curselection()][0]
			Note_Contents.delete('1.0','end')
			Note_Contents.insert('1.0', cur.execute('SELECT contents FROM notes WHERE name = ? AND user = ?', (Note.selection, cur.execute('SELECT username FROM current').fetchone()[0])).fetchone()[0])

		# log out
		def Log_Out():
			remove_error()
			# clear list box and note contents
			Note.Notes_List.delete(0, tk.END)
			Note_Contents.delete('1.0', 'end')
			# delete the current user from database
			cur.execute('DELETE FROM current WHERE username = ?', (cur.execute('SELECT username FROM current').fetchone()[0], ))
			con.commit()
			# resets title
			controller.title('Note Application')
			# go back to start
			controller.show_frame(Start)

		# new note
		def New_Note():
			remove_error()
			# repack the notecreation's contents needed for new note functions (not old name frame packed for this button)
			NoteCreation.Old_Name.pack_forget()
			NoteCreation.Name_Frame.pack_forget()
			NoteCreation.Submit_button.pack_forget()
			NoteCreation.Error_Frame = ttk.Frame(NoteCreation.Master_Frame)
			NoteCreation.Error_Frame.pack()
			NoteCreation.Name_Frame.pack(padx=15, pady=10)
			NoteCreation.Submit_button.pack(fill='x', padx=15, pady=10)
			# go to note creation page
			controller.show_frame(NoteCreation)

		def Rename_Note():
			remove_error()
			if Note.Notes_List.curselection():
				# repacks the notecreation's contents needed for rename (Old name is pack to show the current name you have)
				NoteCreation.Old_Name.pack_forget()
				NoteCreation.Name_Frame.pack_forget()
				NoteCreation.Submit_button.pack_forget()
				NoteCreation.Error_Frame = ttk.Frame(NoteCreation.Master_Frame)
				NoteCreation.Error_Frame.pack()
				NoteCreation.Old_Name.pack(padx=15, pady=10)
				NoteCreation.Name_Frame.pack(padx=15, pady=10)
				NoteCreation.Submit_button.pack(fill='x', padx=15, pady=10)
				NoteCreation.text.set(Note.selection)
				#go to notecreation page
				controller.show_frame(NoteCreation)

			else:
				# show error if no note is selected
				nofile = ttk.Label(Error_Frame, text='no note selected, can\'t rename', foreground='red')
				nofile.pack()
				emessage.append(nofile)

		def Save(quit):
			remove_error()
			if hasattr(Note, 'selection'):
				# save note to database
				cur.execute('UPDATE notes SET contents = ? WHERE name = ? AND user = ?', (Note_Contents.get('1.0', tk.END)[:-1], Note.selection, cur.execute('SELECT username FROM current').fetchone()[0]))
				con.commit()

				# if save and quit button is pressed this will run and exit the application after saving
				if quit == True:
					GUI.destroy(GUI.ins)
			else:
				# give error if no note selected
				nofile = ttk.Label(Error_Frame, text='no note selected, can\'t save', foreground='red')
				nofile.pack()
				emessage.append(nofile)

		def Delete():
			remove_error()
			if hasattr(Note, 'selection'):
				# Deletes a note from the database
				cur.execute('DELETE FROM notes WHERE name =? AND user =?', (Note.selection, cur.execute('SELECT username FROM current').fetchone()[0]))
				con.commit()
				# clears the note contents
				Note_Contents.delete('1.0', 'end')
				# removes the notes name from the list box
				for index, i in enumerate(Note.Notes_List.get(0, tk.END)):
					if i == Note.selection:
						Note.Notes_List.delete(index)

			else:
				# gives error if not note is selected
				nofile = ttk.Label(Error_Frame, text='no note selected, can\'t delete', foreground='red')
				nofile.pack()
				emessage.append(nofile)
			
		# GUI, all widgets

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

		Delete_Button = ttk.Button(Save_Button_frame, text='Delete', width=11, command=Delete)
		Delete_Button.pack(side='right', padx=4)

		Note_Frame = tk.Frame(right_frame)
		Note_Frame.pack(expand=1, fill='both')

		Note_Contents = tk.Text(Note_Frame, wrap='word', font='calibri 12')
		Note_Contents.pack(side='left', expand=1,fill='both')

		scrollbar = tk.Scrollbar(Note_Frame, orient='vertical', command=Note_Contents.yview)
		scrollbar.pack(side='right', fill='y')

		Note_Contents['yscrollcommand'] = scrollbar.set

class NoteCreation(tk.Frame):
	def __init__(self,parent, controller):
		tk.Frame.__init__(self, parent)

		# removes error and goes back to note page triggered with back button
		def back():
			remove_error()
			NoteCreation.Error_Frame.pack_forget()
			Name_Entry.delete(0, tk.END)
			controller.show_frame(Note)

		# creates the note or renames it based on if the old name frame is packed
		def create_note_rename(event):
			remove_error()
			# bad characters
			badchars = [i for i in Name_Entry.get() if i == '\\' or i =='/' or i == ':' or i == '*' or i =='?' or i =='"' or i =='<' or i =='>' or i == '|']
			if badchars:
				Name_Entry.delete(0, tk.END)
				unusablechars = ttk.Label(NoteCreation.Error_Frame, text='can\'t use\n\/:*?"<>|', foreground='red')
				unusablechars.pack()
				emessage.append(unusablechars)
				return None

			# nothing entered
			if Name_Entry.get() == '':
				Name_Entry.delete(0, tk.END)
				nochars = ttk.Label(NoteCreation.Error_Frame, text='no charecters typed', foreground='red')
				nochars.pack()
				emessage.append(nochars)
				return None

			# too long
			if len(Name_Entry.get()) > 35:
				Name_Entry.delete(0, tk.END)
				Notetoolong = ttk.Label(NoteCreation.Error_Frame, text='too long to be displayed', foreground='red')
				Notetoolong.pack()
				emessage.append(Notetoolong)
				return None

			# sees if old name frame is packed and if it is it will rename the selected note
			if NoteCreation.Old_Name.winfo_ismapped():
				if cur.execute('SELECT name FROM notes').fetchone():
					# see if the note already exist for that particular user and gives a error if it already does
					for i in cur.execute('SELECT name FROM notes WHERE user =?', (cur.execute('SELECT username FROM current').fetchone()[0], )).fetchall():
						if i[0] == Name_Entry.get():
							Note_exist = ttk.Label(NoteCreation.Error_Frame, text='that note already exist', foreground='red')
							Note_exist.pack()
							Name_Entry.delete(0, tk.END)
							return
				
				# change the name in the noteslist on the note page
				for index, i in enumerate(Note.Notes_List.get(0, tk.END)):
					if i == Note.selection:
						Note.Notes_List.delete(index)
						Note.Notes_List.insert(tk.END, Name_Entry.get())
				# change the notes name
				cur.execute('UPDATE notes SET name = ? WHERE name = ?', (Name_Entry.get(), Note.selection))
				con.commit()
				# deletes entry box contents
				Name_Entry.delete(0, tk.END)
				remove_error()
				NoteCreation.Error_Frame.pack_forget()
				Note.selection = Name_Entry.get()
				# go back to Note window
				controller.show_frame(Note)

			else:
				# if Old name is not mapped it will create a new note
				if cur.execute('SELECT name FROM notes').fetchone():
					# see if note name exist
					for i in cur.execute('SELECT name FROM notes WHERE user =?', (cur.execute('SELECT username FROM current').fetchone()[0], )).fetchall():
						if i[0] == Name_Entry.get():
							Note_exist = ttk.Label(NoteCreation.Error_Frame, text='that note already exist', foreground='red')
							Note_exist.pack()
							Name_Entry.delete(0, tk.END)
							return
				
				# adds it to notes list on Note page
				Note.Notes_List.insert(tk.END, Name_Entry.get())
				# put it in the database	
				cur.execute('INSERT INTO notes VALUES(?, ?, ?)', (cur.execute('SELECT username FROM current').fetchone()[0], Name_Entry.get(), ''))
				con.commit()
				# clear entry box
				Name_Entry.delete(0, tk.END)
				remove_error()
				NoteCreation.Error_Frame.pack_forget()
				# go back to Note page
				controller.show_frame(Note)

		# GUI for the NoteCreation page

		Back_Button = ttk.Button(self, text='Back', command=back)
		Back_Button.place(x=10,y=10)

		NoteCreation.Master_Frame = tk.Frame(self, borderwidth='2', relief='groove')
		NoteCreation.Master_Frame.pack(expand=1)

		NoteCreation.Error_Frame = tk.Frame(NoteCreation.Master_Frame)
		NoteCreation.Error_Frame.pack()

		NoteCreation.Old_Name = tk.Frame(NoteCreation.Master_Frame)
		NoteCreation.Old_Name.pack(padx=15, pady=10)

		Old_Label = ttk.Label(NoteCreation.Old_Name, text='old note\'s name:', font='calibri 10  bold underline')
		Old_Label.pack()

		NoteCreation.text = tk.StringVar()
		NoteCreation.text.set('')
		NoteCreation.Old_file_name = ttk.Label(NoteCreation.Old_Name, textvariable=NoteCreation.text, font='calibri 11')
		NoteCreation.Old_file_name.pack()

		NoteCreation.Name_Frame = tk.Frame(NoteCreation.Master_Frame)
		NoteCreation.Name_Frame.pack(padx=15, pady=15)

		Name_Label = ttk.Label(NoteCreation.Name_Frame, text='Name:')
		Name_Label.pack(side='left')

		Name_Entry = ttk.Entry(NoteCreation.Name_Frame, width=40)
		Name_Entry.pack(side='right')
		Name_Entry.bind('<Return>', create_note_rename)

		# the 'a' variable passed in does nothing but the function has a parameter so it's needed
		NoteCreation.Submit_button = ttk.Button(NoteCreation.Master_Frame, text='Submit', command=lambda:create_note_rename('a'))
		NoteCreation.Submit_button.pack(fill='x')

app = GUI()
app.mainloop()
