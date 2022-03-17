import tkinter as tk
from tkinter import ttk

from database_methods import create_connection, execute_query, read_query
import sign_in

window=tk.Tk()
window.title("Forgot your password")
window.geometry("500x400")

#Method for button 'Clear'
def clear():
    username_ent.delete(0,tk.END)
    sec_question.set("")
    secans_ent.delete(0,tk.END)

#Method for button 'Next'
def next():
    connection=create_connection("mydatabase.db")
    select=f"SELECT username,security_question,security_answer from login"
    entries=read_query(connection,select)
    u=username_ent.get()
    sq=sec_question.get()
    sa=secans_ent.get()
    if (u,sq,sa) in entries:
        btn_next.destroy()
        btn_clear.destroy()
        #Method for Create Password
        def create():
            #Update the information
            np=ent_3.get()
            npr=ent_4.get()
            if np==npr:
                update_password=f"UPDATE login SET password='{np}'"
                execute_query(connection,update_password)
                window.destroy()
            else:
                frame4=tk.Frame(master=window)
                lbl=tk.Label(master=frame4, text="Passwords do not coincide. Please try again")
                frame4.pack()
                lbl.pack()

        lbl_3=tk.Label(master=frame2,text=labels[3],font=("Times New Roman", 17))
        lbl_4=tk.Label(master=frame2,text=labels[4],font=("Times New Roman", 17))
        ent_3=tk.Entry(master=frame2,show="*")
        ent_4=tk.Entry(master=frame2,show="*")
        lbl_3.grid(row=3,column=0,sticky="e")
        lbl_4.grid(row=4,column=0,sticky="e")
        ent_3.grid(row=3,column=1,sticky="ew")
        ent_4.grid(row=4,column=1,sticky="ew")
        #Method for button 'Clear2'
        def clear2():
            username_ent.delete(0,tk.END)
            sec_question.set("")
            secans_ent.delete(0,tk.END)
            ent_3.delete(0,tk.END)
            ent_4.delete(0,tk.END)
        btn_clear2=tk.Button(master=frame3,text="Clear",command=clear2)
        btn_create=tk.Button(master=frame3,text="Create New Password",command=create)
        btn_clear2.grid(row=0,column=0,sticky="ew")
        btn_create.grid(row=0,column=1,sticky="ew")
    else:
        frame4=tk.Frame(master=window)
        lbl=tk.Label(master=frame4, text="The data entered is not correct. Please try again.")
        frame4.pack()
        lbl.pack()

#Create a Frame for the title
frame1=tk.Frame(master=window)
lbl=tk.Label(master=frame1, fg="blue", font=("Times New Roman",44), text="Recover your password")
frame1.pack()
lbl.pack(pady=5,padx=5)

#Create a Frame for the form
frame2=tk.Frame(master=window)
frame2.pack()
labels=["Username","Security Question","Answer","New Password", "Confirm New Password"]
questions=["What is your mother's middle name?", "What is the name of your high school?",
"What is the name of your first pet?", "What is your favourite colour?"]

for i in range(3):
    lbl_i=tk.Label(master=frame2, text=labels[i],font=("Times New Roman", 17))
    lbl_i.grid(row=i,column=0,sticky="e")

username_ent=tk.Entry(master=frame2)
sec_question=ttk.Combobox(master=frame2, values=questions,state="readonly")
secans_ent=tk.Entry(master=frame2)
username_ent.grid(row=0,column=1,sticky="ew")
sec_question.grid(row=1,column=1,sticky="ew")
secans_ent.grid(row=2,column=1,sticky="ew")

#Create a Frame for the Buttons
frame3=tk.Frame(master=window)
frame3.pack()
btn_clear=tk.Button(master=frame3, text="Clear",command=clear)
btn_clear.grid(row=0,column=0,sticky="nsew")

btn_next=tk.Button(master=frame3,text="Next",command=next)
btn_next.grid(row=0,column=1,sticky="ew")
window.mainloop()
