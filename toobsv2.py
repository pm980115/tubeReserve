import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('tubes.db') #connect to db fie

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dateOf(
	rDate text PRIMARY KEY
	)
	""")
#create tables
c.execute("""CREATE TABLE IF NOT EXISTS reservation( 
	phone text PRIMARY KEY,
	name text,
	numPeople integer,
	numCooler integer,
	rTime text,
	rDate text NOT NULL,
	FOREIGN KEY (rDate)
		REFERENCES dateOf (rDate)
	)
	""")
c.execute("INSERT INTO dateOf VALUES ('04-20-2020')")
c.execute("INSERT INTO dateOf VALUES ('04-21-2020')")
c.execute("INSERT INTO dateOf VALUES ('04-22-2020')")
c.execute("INSERT INTO dateOf VALUES ('04-23-2020')")
c.execute("INSERT INTO reservation VALUES ('555-555-5555', 'Pat M', 1, 0, '12pm', '04-20-2020')")
c.execute("INSERT INTO reservation VALUES ('555-555-5556', 'Pat O', 1, 0, '11pm', '04-20-2020')")
class tubes(tk.Tk): # class handles multiple pages by creating frames to switch through
	
	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand = True)

		self.frames = {}

		for F in (StartPage, checkPage, makePage):
			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, container):
		frame = self.frames[container]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text = "Welcome to Pat's Tube Reservation Program! \nChoose whether you would like to look at reservations, or create a new one", font = ("Helvetica", "16"))
		label.pack()

		results = tk.Listbox()
		c.execute('SELECT * from dateOf')
		
		i = 1
		for d in c.fetchall(): #read in dates from db and populate listbox
			results.insert(i, d)
			i+=1
		cs = results.curselection()
		results.bind('<Double-1>', lambda event, arg=results: self.search(event, arg))
		results.pack()

		check = tk.Button(self,
		    text="Check Reservations",
		    width=15,
		    height=1,
		    bg="blue",
		    fg="yellow",
		    command=lambda: controller.show_frame(checkPage)
		)
		make = tk.Button(self,
		    text="Make Reservations",
		    width=15,
		    height=1,
		    bg="blue",
		    fg="yellow",
		    command=lambda: controller.show_frame(makePage)
		)

		check.pack()
		make.pack()
	def search(self, event, arg):
		#out.pack_forget()
		cs = arg.curselection()
		txt = arg.get(cs)
		txt = str(txt).strip('(').strip(')').strip('\'').strip(',').strip("'")
		print(txt)
		c.execute('SELECT * from reservation where rDate= "' + txt + '"' )
		r = c.fetchall()
		print(r)
		out = tk.Listbox(width=50)
		j=0 #acc
		for i in r: #i = item in list r = list of reservations
			out.insert(j, i)
			j+=1
		out.pack()
		

class checkPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text = "Look at Reservations \n Enter a date in MM-DD-YYYY format, e.g. July 28th 2020 is 07-28-2020", font = ("Helvetica", "16"))
		label.pack()
		reservations = tk.Listbox()
		txt = tk.Entry(self, width = 25)
		txt.pack()
		r = ''
		look = tk.Button(self,
		    text="Look up date",
		    width=15,
		    height=1,
		    bg="blue",
		    fg="yellow",
		    command=lambda: search(txt.get())
		)
		look.pack()
		back = tk.Button(self,
		    text="Back to Home",
		    width=15,
		    height=1,
		    bg="red",
		    fg="black",
		    command=lambda: controller.show_frame(StartPage)
		)
		back.pack()

def search(event, arg):
	cs = txt.curselection()
	c.execute('SELECT * from reservation where rDate=' + txt )
	r = c.fetchall()


class makePage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text = "Create a Reservation", font = ("Helvetica", "16"))
		label.pack()
		back = tk.Button(self,
		    text="Back to Home",
		    width=15,
		    height=1,
		    bg="red",
		    fg="black",
		    command=lambda: controller.show_frame(StartPage)
		)
		back.pack()
app = tubes()
app.mainloop()