import tkinter as tk
from tkinter import ttk

from database_methods import create_connection, execute_query, read_query

homepage=tk.Tk()
homepage.title("Homepage")
homepage.geometry('400x400')

#Method for 'Clear' button
def clear():
    username_ent.delete(0,tk.END)
    password_ent.delete(0,tk.END)

#Continue Method
def cont():
    connection=create_connection("mydatabase.db")
    select=f"SELECT username, password from login"
    entries=read_query(connection,select)
    u=username_ent.get()
    p=password_ent.get()
    #Check if 'username' and 'password' are valid
    if (u,p) in entries:
        frame_password=tk.Frame(master=homepage, relief=tk.RAISED)
        lbl=tk.Label(master=frame_password, text="Correct!")
        frame_password.grid(row=5)
        lbl.grid(row=2)
        homepage.destroy()
    else:
        def forgot():
            homepage.destroy()
        frame_password=tk.Frame(master=homepage, relief=tk.RAISED)
        lbl=tk.Label(master=frame_password, text="Wrong username or password")
        btn=tk.Button(master=frame_password, text="Forgot your password?",command=forgot)
        frame_password.grid(row=5)
        lbl.grid(row=0,column=0)
        btn.grid(row=0,column=1)

#Show/Hide password
def show_hide():
    if password_ent["show"]=="*":
        password_ent["show"]=""
    elif password_ent["show"]=="":
        password_ent["show"]="*"

#Frame to sign in
framelbl=tk.Frame(master=homepage)
framelbl.grid(row=0)
lbl=tk.Label(master=framelbl, fg="blue",text="Sign in",font=("Times New Roman", 44))
lbl.grid(row=0)

signin=ttk.Frame(master=homepage, relief = tk.FLAT, borderwidth = 1)
signin.grid(row=1)

labels=["Username", "Password"]
for i in range(2):
    label_i=tk.Label(master=signin, text=labels[i],font=("Times New Roman", 17))
    label_i.grid(row=i, column=0,sticky="e")

username_ent=tk.Entry(master=signin)
password_ent=tk.Entry(master=signin,show="*")
username_ent.grid(row=0,column=1)
password_ent.grid(row=1,column=1)

show_hide=tk.Button(master=signin, text="Show/Hide",command=show_hide)
show_hide.grid(row=1,column=2)

#Frame for the Buttons
frame2=tk.Frame(master=homepage, relief=tk.RAISED)
frame2.grid(row=2)

btn_clear=tk.Button(master=frame2, text="Clear",command=clear)
btn_clear.grid(row=0,column=0,sticky="ew")

btn_cont=tk.Button(master=frame2,text="Continue",command=cont)
btn_cont.grid(row=0,column=1,sticky="ew")

#Frame for the Registration
frame3=tk.Frame(master=homepage)
frame3.grid(row=3)

lbl=tk.Label(master=frame3,width=400, height=100)


reg=tk.Button(master=homepage,text="Register here!", command=homepage.destroy)
reg.grid(row=4)

homepage.mainloop()
