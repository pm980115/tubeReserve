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
c.execute("INSERT INTO reservation VALUES ('550-555-5555', 'Mat S', 1, 0, '12pm', '04-21-2020')")
c.execute("INSERT INTO reservation VALUES ('551-555-5556', 'Mat P', 1, 0, '11pm', '04-21-2020')")
c.execute("INSERT INTO reservation VALUES ('550-555-5055', 'Rat G', 1, 0, '12pm', '04-21-2020')")
c.execute("INSERT INTO reservation VALUES ('551-555-5156', 'Rat K', 1, 0, '11pm', '04-21-2020')")


window = tk.Tk()
window.geometry('900x750')
window.title("Pat's Tube Reservation Program")
intruct = tk.Label(window, text = "Welcome to Pat's Tube Reservation Program! \nDouble click a date on the left to see the reservations for that day, or create a new one", font = ("Helvetica", "10"))
intruct.grid(row=0, column=1, sticky='ew')

reservationLabels = tk.Label(window, text="Phone Number, Name, Size of Party, # of Coolers, Time, Date")
reservationLabels.grid(row=1, column=1, sticky='n')


dates = tk.Listbox(height=30)
c.execute('SELECT * from dateOf')

people = tk.Listbox(width=50, height=30)


i = 1
for d in c.fetchall(): #read in dates from db and populate listbox
	dates.insert(i, d)
	i+=1
cs = dates.curselection()
dates.bind('<Double-1>', lambda event, arg=dates: search(window, event, arg))
dates.grid(row=2, column=0, sticky='w')
people.grid(row=2, column=1)


def search(self, event, arg):
	people.delete(0,100)
	cs = arg.curselection()
	txt = arg.get(cs)
	txt = str(txt).strip('(').strip(')').strip('\'').strip(',').strip("'")#manipulate string to be read by sqlite
	print(txt)
	c.execute('SELECT * from reservation where rDate= "' + txt + '"' )
	r = c.fetchall()
	print(r)
	j=0 #acc
	for i in r: #i = item in list r = list of reservations
		people.insert(j, i)
		j+=1
	people.grid(row=2, column=1)

newNum = tk.Entry(window, width = 25)
newName = tk.Entry(window, width = 25)
newNumP= tk.Entry(window, width = 25)
newNumC = tk.Entry(window, width = 25)
newTime = tk.Entry(window, width = 25)
newDate = tk.Entry(window, width = 25)

inputInstruct = tk.Label(window, text = "To add a new reservation enter the information below")
labelNewNum = tk.Label(window, text = " Phone Number")
labelNewName = tk.Label(window, text = "Name")
labelNewNumP= tk.Label(window, text = "Number of People")
labelNewNumC = tk.Label(window, text = "Number of Coolers")
labelNewTime = tk.Label(window, text = "Time")
labelNewDate = tk.Label(window, text = "Date (please enter in MM-DD-YYYY form")

labelNewNum.grid(row=3, column=0, sticky='w')
labelNewName.grid(row=4, column=0, sticky='w')
labelNewNumP.grid(row=5, column=0, sticky='w')
labelNewNumC.grid(row=6, column=0, sticky='w')
labelNewTime.grid(row=7, column=0, sticky='w')
labelNewDate.grid(row=8, column=0, sticky='w')

newNum.grid(row=3, column=1, sticky='w')
newName.grid(row=4, column=1, sticky='w')
newNumP.grid(row=5, column=1, sticky='w')
newNumC.grid(row=6, column=1, sticky='w')
newTime.grid(row=7, column=1, sticky='w')
newDate.grid(row=8, column=1, sticky='w')

addReservation = tk.Button(window,
		    text="Add Reservation",
		    width=15,
		    height=1,
		    bg="blue",
		    fg="yellow",
		    command=lambda: add(newNum.get(), newName.get(), newNumP.get(), newNumC.get(), newTime.get(), newDate.get())
		)
addReservation.grid(row=9, column=1)
def add(num, name, numPeople, numCooler, time, date):

	c.execute('INSERT INTO reservation VALUES ("' + num + '", "' + name + '", "' + numPeople + '", "' + numCooler + '", "' + time + '", "' + date +'")')
	conn.commit()
	j=0 #acc
	for i in r: #i = item in list r = list of reservations
		people.insert(j, i)
		j+=1
	people.grid(row=2, column=1)


window.mainloop()