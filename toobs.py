import sqlite3
from tkinter import *

conn = sqlite3.connect('tubes.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dateOf(
	rDate text PRIMARY KEY
	)
	""")

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

#c.execute("INSERT INTO dateOf VALUES ('04-20-2020')")
#c.execute("INSERT INTO reservation VALUES ('555-555-5555', 'Pat M', 1, 0, '12pm', '04-20-2020')")

window = Tk()
window.geometry('750x200')
window.title("Pat's Tube Reservation Program")
intruct = Label(window, text = "Welcome to Pat's Tube Reservation Program! \nChoose whether you would like to look at reservations, or create a new one", font = ("Helvetica", "16"))
intruct.pack()
check = Button(window,
    text="Check Reservations",
    width=15,
    height=1,
    bg="blue",
    fg="yellow",
)
make = Button(window,
    text="Make Reservations",
    width=15,
    height=1,
    bg="blue",
    fg="yellow",
)

check.pack()
make.pack()
window.mainloop()

c.execute("SELECT * from reservation")

print("  Number          Name  #people #cooler  time  date ")
print(c.fetchall())

conn.commit()
conn.close()