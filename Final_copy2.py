from tkinter import *
from PIL import Image
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import tkinter
import time

# splash screen
splash = Tk()
splash.title('Splash')
splash.geometry('400x200')
splash.geometry('+460+260')
splash.overrideredirect(True)

s_frame=Frame(splash, bg='#202020', width=400, height=200)
s_frame.pack()

img = PhotoImage(file='pic.png')
lbl1= Label(s_frame, image = img, bg='#202020')
lbl1.place(x=100, y=50, anchor=NE)

lbl2 = Label(s_frame, text="Patient Information", font=(' ', 14), fg='#F0F0F0', bg='#202020')
lbl2.place(x=320, y=60, anchor=NE)

lbl3 = Label(s_frame, text="System", font=(' ', 17), fg='#F0F0F0', bg='#202020')
lbl3.place(x=280, y=90, anchor=NE)

splash.update()

time.sleep(3)
splash.destroy()

class Tk(tkinter.Tk):

    def __init__(self,master=None):
        tkinter.Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

# main screen
root = Tk()
root.title('Title')
root.geometry('720x565')
root.geometry('+300+100')

root.deiconify()

style = ttk.Style(root)

left = Frame(root,bg='#202020', width = 200, height = 565)
left.pack(side = LEFT)
right = Frame(root, width = 520, height = 308)
right.pack(side = TOP)
bottom = Frame(root, width = 520, height = 175)
bottom.pack(side = BOTTOM)

# radio button checking
def radio():
    if rad_sel.get()==1:
        rad = 'm'
        print(rad)
        return rad
    else:
        rad = 'f'
        print(rad)
        return rad

# checkbox checking
def check():
    if chk_sel1.get()==1:
        chk = 'O+ve'
        print(chk)
        return chk
    elif chk_sel2.get()==1:
        chk = 'O-ve'
        print(chk)
        return chk
    elif chk_sel3.get()==1:
        chk = 'A+ve'
        print(chk)
        return chk
    elif chk_sel4.get()==1:
        chk = 'A-ve'
        print(chk)
        return chk
    elif chk_sel5.get()==1:
        chk = 'B+ve'
        print(chk)
        return chk
    elif chk_sel6.get()==1:
        chk = 'B-ve'
        print(chk)
        return chk
    elif chk_sel7.get()==1:
        chk = 'AB+ve'
        print(chk)
        return chk
    elif chk_sel8.get()==1:
        chk = 'AB-ve'
        print(chk)
        return chk

# databse name
db_name = 'database.db'

# messagebox for add
def clk_add1():
    messagebox.showinfo(' ', 'Data Added Successfully !')    
def clk_add2():
    messagebox.showinfo(' ', 'Fields Are Empty')
# messagebox for delete
def clk_del1():
    messagebox.showinfo(' ', 'Data Deleted Successfully !')
def clk_del2():
    messagebox.showinfo(' ', 'Please Select Record')
# messagebox for update
def clk_up():
    messagebox.showinfo(' ', 'Data Updated Successfully !')
    
# database query
def run_query(query, parameters = ()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result

# viewing records from database
def viewing_records():
    
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    query = 'SELECT * FROM patient ORDER by id DESC'
    db_rows = run_query(query)
    for row in db_rows:
        tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3],
                                                    row[4], row[5], row[6]))

# validation
def validation():
    return len(txt5.get()) != 0

# adding data in database
def adding():
    if validation():
        rad = radio()
        print(rad)
        chk = check()
        print(chk)
        query = 'INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?, ?)'
        parameters = (txt5.get(), txt3.get(), txt4.get(),
                      txt6.get(), txt7.get(), rad, chk)
        run_query(query, parameters)
        clk_add1()
        txt3.delete(0, END)
        txt4.delete(0, END)
        txt5.delete(0, END)
        txt6.delete(0, END)
        txt7.delete(0, END)

    else:
        clk_add2()
    viewing_records()

# deleting data from database
def deleting():
    try:
        tree.item(tree.selection())['values'][0]
    except IndexError as e:
        clk_del2()
        return
    name = tree.item(tree.selection())['text']
    query = 'DELETE FROM patient WHERE id = ?'

    run_query(query, (name, ))
    clk_del1()
    viewing_records()

def close(event):
    root.destroy()
    print('Exited')
    
def edit_fname(new_txt1, fname):
    query = 'UPDATE patient SET fname=? WHERE fname=?'
    parameters = (new_txt1, fname)
    run_query(query, parameters)
    viewing_records()
    clk_up()

def edit_lname(new_txt2, lname):
    query = 'UPDATE patient SET lname=? WHERE lname=?'
    parameters = (new_txt2, lname)
    run_query(query, parameters)
    viewing_records()
    clk_up()

def edit_height(new_txt3, h):
    query = 'UPDATE patient SET height=? WHERE height=?'
    parameters = (new_txt3, h)
    run_query(query, parameters)
    viewing_records()
    clk_up()

def edit_weight(new_txt4, w):
    query = 'UPDATE patient SET weight=? WHERE weight=?'
    parameters = (new_txt4, w)
    run_query(query, parameters)
    print(new_txt4)
    viewing_records()
    clk_up()

def editing():
    try:
        tree.item(tree.selection())['values'][1]
    except IndexError as e:
        clk_del2()
        return
    
    fname = tree.item(tree.selection())['values'][0]
    lname = tree.item(tree.selection())['values'][1]
    h = tree.item(tree.selection())['values'][2]
    w = tree.item(tree.selection())['values'][3]

    # creating new window
    update=Toplevel()
    update.title('Update Data')
    update.geometry('300x150')

    # notebook
    tab_control = ttk.Notebook(update)
 
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
 
    tab_control.add(tab1, text='First Name')
    tab_control.add(tab2, text='Last Name')
    tab_control.add(tab3, text='Height')
    tab_control.add(tab4, text='Weight')
 
    #update fname
    old_fname = Label(tab1, text='Old First Name')
    old_fname.grid(row=1,column=1)
    old_txt1 = Label(tab1, textvariable=StringVar(tab1, value=fname))
    old_txt1.grid(row=1, column=2)

    new_fname = Label(tab1, text='New First Name')
    new_fname.grid(row=2,column=1)
    new_txt1 = Entry(tab1)
    new_txt1.grid(row=2, column=2)

    btn = Button(tab1,text='Save changes', command=lambda:edit_fname(new_txt1.get(), fname))
    btn.grid(row=3,column=2,sticky = W)

    #update lname
    old_lname = Label(tab2, text='Old Last Name')
    old_lname.grid(row=1,column=1)
    old_txt2 = Label(tab2, textvariable=StringVar(tab2, value=lname))
    old_txt2.grid(row=1, column=2)

    new_lname = Label(tab2, text='New Last Name')
    new_lname.grid(row=2,column=1)
    new_txt2 = Entry(tab2)
    new_txt2.grid(row=2, column=2)

    btn = Button(tab2,text='Save changes', command=lambda:edit_lname(new_txt2.get(), lname))
    btn.grid(row=3,column=2,sticky = W)

    #update height
    old_height = Label(tab3, text='Old Height')
    old_height.grid(row=1,column=1)
    old_txt3 = Label(tab3, textvariable=StringVar(tab3, value=h))
    old_txt3.grid(row=1, column=2)

    new_height = Label(tab3, text='New Height')
    new_height.grid(row=2,column=1)
    new_txt3 = Entry(tab3)
    new_txt3.grid(row=2, column=2)

    btn = Button(tab3,text='Save changes', command=lambda:edit_height(new_txt3.get(), h))
    btn.grid(row=3,column=2,sticky = W)

    #update weight
    old_weight = Label(tab4, text='Old Weight')
    old_weight.grid(row=1,column=1)
    old_txt4 = Label(tab4, textvariable=StringVar(tab4, value=w))
    old_txt4.grid(row=1, column=2)

    new_weight = Label(tab4, text='New Weight')
    new_weight.grid(row=2,column=1)
    new_txt4 = Entry(tab4)
    new_txt4.grid(row=2, column=2)

    btn = Button(tab4,text='Save changes', command=lambda:edit_weight(new_txt4.get(), w))
    btn.grid(row=3,column=2,sticky = W)
 
    tab_control.pack(expand=1, fill='both')

    update.mainloop()

#labels and textboxes

lbl9 = Label(right, bg='#202020')
lbl9.place(x=500, y=0, anchor=NE, width=530, height=28)

lbl10 = Label(right, bg='#202020')
lbl10.place(x=520, y=28, anchor=NE, width=5, height=300)

lbl11 = Label(bottom, bg='#202020')
lbl11.place(x=520, y=0, anchor=NE, width=5, height=252)

lbl12 = Label(bottom, bg='#202020')
lbl12.place(x=550, y=252, anchor=NE, width=550, height=5)

img = PhotoImage(file='pic.png')
lbl1 = Label(left, image = img, bg='#202020', fg='white')
lbl1.place(x=135, y=130, anchor=NE)

img2 = PhotoImage(file='pic2.png')
lbl8 = Label(right, image = img2, bg='#202020')
lbl8.place(x=520, y=0, anchor=NE)
lbl8.bind("<Button-1>",close)

lbl2 = Label(left, text="Patient Information System", fg='#F0F0F0', bg='#202020')
lbl2.place(x=155, y=0, anchor=NE)

lbl2 = Label(left, text="Patient", font=("Helvetica", 14), fg='#F0F0F0', bg='#202020')
lbl2.place(x=130, y=250, anchor=NE)
lbl2 = Label(left, text="Information", font=("Helvetica", 14), fg='#F0F0F0', bg='#202020')
lbl2.place(x=150, y=280, anchor=NE)
lbl2 = Label(left, text="System", font=("Helvetica", 14), fg='#F0F0F0', bg='#202020')
lbl2.place(x=135, y=310, anchor=NE)

lbl3 = Label(right, text='First Name')
lbl3.place(x=160, y=80, anchor=NE)
txt3 = Entry(right, width=11)
txt3.place(x=240, y=80, anchor=NE)

lbl4 = Label(right, text='Last Name')
lbl4.place(x=310, y=80, anchor=NE)
txt4 = Entry(right, width=11)
txt4.place(x=390, y=80, anchor=NE)

lbl5 = Label(right, text='Patient ID.')
lbl5.place(x=140, y=120, anchor=NE)
txt5 = Entry(right, width=11)
txt5.place(x=220, y=120, anchor=NE)

lbl6 = Label(right, text='Height')
lbl6.place(x=270, y=120, anchor=NE)
txt6 = Entry(right, width=5)
txt6.place(x=325, y=120, anchor=NE)

lbl7 = Label(right, text='Weight')
lbl7.place(x=370, y=120, anchor=NE)
txt7 = Entry(right, width=5)
txt7.place(x=415, y=120, anchor=NE)

# radio buttons
rad_sel = IntVar()
rad1 = Radiobutton(right,text='Male', value=1, variable=rad_sel, command=radio)
rad2 = Radiobutton(right,text='Female', value=2, variable=rad_sel, command=radio)
rad1.place(x=230, y=160, anchor=NE)
rad2.place(x=310, y=160, anchor=NE)

#check buttons
chk_sel1 = IntVar()
chk1 = Checkbutton(right, text = 'O+ve', variable=chk_sel1, command=check, onvalue=1, offvalue=0)
chk1.place(x=190, y=200, anchor=NE)
chk_sel2 = IntVar()
chk2 = Checkbutton(right, text = 'O-ve', variable=chk_sel2, command=check, onvalue=1, offvalue=0)
chk2.place(x=255, y=200, anchor=NE)
chk_sel3 = IntVar()
chk3 = Checkbutton(right, text = 'A+ve', variable=chk_sel3, command=check, onvalue=1, offvalue=0)
chk3.place(x=320, y=200, anchor=NE)
chk_sel4 = IntVar()
chk4 = Checkbutton(right, text = 'A-ve', variable=chk_sel4, command=check, onvalue=1, offvalue=0)
chk4.place(x=383, y=200, anchor=NE)
chk_sel5 = IntVar()
chk5 = Checkbutton(right, text = 'B+ve', variable=chk_sel5, command=check, onvalue=1, offvalue=0)
chk5.place(x=187, y=220, anchor=NE)
chk_sel6 = IntVar()
chk6 = Checkbutton(right, text = 'B-ve', variable=chk_sel6, command=check, onvalue=1, offvalue=0)
chk6.place(x=253, y=220, anchor=NE)
chk_sel7 = IntVar()
chk7 = Checkbutton(right, text = 'AB+ve', variable=chk_sel7, command=check, onvalue=1, offvalue=0)
chk7.place(x=327, y=220, anchor=NE)
chk_sel8 = IntVar()
chk8 = Checkbutton(right, text = 'AB-ve', variable=chk_sel8, command=check, onvalue=1, offvalue=0)
chk8.place(x=390, y=220, anchor=NE)

# buttons
btn1= Button(right, text="Add Data", command = adding)
btn1.place(x=190, y=260, anchor=NE)

btn2 = Button(right, text="Delete Data", command = deleting)
btn2.place(x=290, y=260, anchor=NE)

btn2 = Button(right, text="Update Data", command = editing)
btn2.place(x=390, y=260, anchor=NE)

# treeview
tree = ttk.Treeview(bottom, height = 10, column = 6)
tree["column"]=('#0','#1','#2','#3','#4','#5')
tree.grid(row = 0, column = 0, columnspan = 6, padx=14, pady=15)

tree.heading('#0', text = 'Patient ID')
tree.column('#0', anchor = 'center', width = 70)
tree.heading('#1', text = 'First Name')
tree.column('#1', anchor = 'center', width = 90)
tree.heading('#2', text = 'Last Name')
tree.column('#2', anchor = 'center', width = 90)
tree.heading('#3', text = 'Height')
tree.column('#3', anchor = 'center', width = 60)
tree.heading('#4', text = 'Weight')
tree.column('#4', anchor = 'center', width = 60)
tree.heading('#5', text = 'M/F')
tree.column('#5', anchor = 'center', width = 40)
tree.heading('#6', text = 'Blood Group')
tree.column('#6', anchor = 'center', width = 80)

viewing_records()

root.mainloop()
