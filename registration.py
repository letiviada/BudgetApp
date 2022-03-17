import tkinter as tk
from tkinter import ttk

from database_methods import create_connection, execute_query, read_query, username_table

window=tk.Tk()
window.title("Homepage")
window.geometry('400x400')

labels=["Username", "Password","Repeat Password","Security Question", "Answer"]
questions=["What is your mother's middle name?", "What is the name of your high school?",
"What is the name of your first pet?", "What is your favourite colour?"]
def clear():
    username_ent.delete(0,tk.END)
    password_ent.delete(0,tk.END)
    passwordcheck_ent.delete(0,tk.END)
    sec_question.set("")
    secans_ent.delete(0,tk.END)


def insert():
    u=username_ent.get()
    p1=password_ent.get()
    p2=passwordcheck_ent.get()
    sq=sec_question.get()
    sa=secans_ent.get()
    connection=create_connection("mydatabase.db")
    # check if the ´username´ already exists in the login table
    check_usernamename = f"SELECT username from login WHERE username='{u}'"
    entries = read_query(connection,check_usernamename)
    if entries == []:
        if p1==p2:
            create_login = f"INSERT INTO login (username,password,security_question,security_answer,expense,income)\
            VALUES ('{u}','{p1}','{sq}','{sa}',0,0)"
            execute_query(connection,create_login)
            username_table(connection,u)
            frame_password=tk.Frame(master=window, relief=tk.RAISED)
            lbl=tk.Label(master=frame_password, text="user added!")
            frame_password.pack()
            lbl.pack()

        else:
            frame_password=tk.Frame(master=window, relief=tk.RAISED)
            lbl=tk.Label(master=frame_password, text="Passwords do not coincide")
            frame_password.pack()
            lbl.pack()
    else:
        frame_password=tk.Frame(master=window, relief=tk.RAISED)
        lbl=tk.Label(master=frame_password, text="username already exists, choose another")
        frame_password.pack()
        lbl.pack()

#Frame for the title
frame=tk.Frame(master=window)
title=tk.Label(master=frame, fg="blue",text="Register here",font=("Times New Roman", 44))
frame.pack()
title.pack()

#Frame for the registration form
frame1=tk.Frame(master=window, relief = tk.FLAT, borderwidth = 1)
frame1.pack()


for i in range(5):
    label_i=tk.Label(master=frame1, text=labels[i],font=("Times New Roman", 17))
    label_i.grid(row=i, column=0,sticky="e")

username_ent=tk.Entry(master=frame1)
password_ent=tk.Entry(master=frame1,show="*")
passwordcheck_ent=tk.Entry(master=frame1,show="*")
sec_question=ttk.Combobox(master=frame1, values=questions,state="readonly")
secans_ent=tk.Entry(master=frame1)
username_ent.grid(row=0,column=1,sticky="ew")
password_ent.grid(row=1,column=1,sticky="ew")
passwordcheck_ent.grid(row=2,column=1, sticky="ew")
sec_question.grid(row=3,column=1,sticky="ew")
secans_ent.grid(row=4,column=1,sticky="ew")
#Frame for the buttons
frame2=tk.Frame(master=window, relief=tk.RAISED)
frame2.pack()

btn_clear=tk.Button(master=frame2, text="Clear",command=clear)
btn_clear.grid(row=0,column=0,sticky="ew")

btn_subm=tk.Button(master=frame2,text="Submit",command=insert)
btn_subm.grid(row=0,column=1,sticky="ew")

window.mainloop()
