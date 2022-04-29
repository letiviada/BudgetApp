import tkinter as tk
from tkinter import ttk
import datetime

from database_methods import create_connection, execute_query, read_query

home=tk.Tk()
home.title("Budget App")
home.geometry("600x500")

#Lists
labels=["Username: ","Category: ","Date: ","Description: ", "Enter your expenses here: ",
 "You have spent: ","Please enter a number above","Enter your income here: ",
  "Total income: ", "Please enter a number above","Balance: "]

categories=["Clothing","Entertainment", "Groceries", "Rent", "Transport/Travel","Other"]

names=["Date","Amount","Description","Category"]

#Method for seeing the expenses using filters
def exp2():
    #Create a table with the filters
    for i in range(4):
        label=tk.Label(master=fr1,text=names[i],width=10)
        label.grid(row=0,column=i,sticky="ew")
    date_ent=tk.Entry(master=fr1,width=10)
    amount_ent=tk.Entry(master=fr1,width=10)
    desc_ent=tk.Entry(master=fr1,width=10)
    categ_ent=ttk.Combobox(master=fr1,values=categories,width=10,state="readonly")
    date_ent.grid(row=1,column=0,sticky="ew")
    amount_ent.grid(row=1,column=1,sticky="ew")
    desc_ent.grid(row=1,column=2,sticky="ew")
    categ_ent.grid(row=1,column=3,sticky="ew")


    #Method for the filter button
    def filter(a=0):
        u=username.get()
        d=date_ent.get()
        a=amount_ent.get()
        de=desc_ent.get().lower()
        c=categ_ent.get()
        connection=create_connection("mydatabase.db")
        if not a:
            cond1=f"SELECT id, amount from '{u}'"
            ent1=read_query(connection,cond1)
            print(ent1)
        else:
            cond1=f"SELECT id, amount from '{u}' WHERE amount>'{a}'"
            ent1=read_query(connection,cond1)
            print(ent1)
        if not de:
            cond2=f"SELECT id, description from '{u}'"
            ent2=read_query(connection,cond2)
            print(ent2)
        else:
            cond2=f"SELECT id, description from '{u}' WHERE description LIKE '%{de}%'"
            ent2=read_query(connection,cond2)
            print(ent2)
        if not c:
            cond3=f"SELECT id,category from '{u}'"
            ent3=read_query(connection,cond3)
            print(ent3)
        else:
            cond3=f"SELECT id,category from '{u}' WHERE category=='{c}'"
            ent3=read_query(connection,cond3)
            print(ent3)

    btn=tk.Button(master=fr1, text="Filter",command=filter)
    btn.grid(row=0,column=4,sticky="ew")
#Method for seeing the expenses
def exp():
    u=username.get()
    for i in range(4):
        label=tk.Label(master=fr1,text=names[i],width=10)
        label.grid(row=0,column=i,sticky="ew")

    get_values=f"SELECT date,amount,category,description from '{u}'"
    connection=create_connection("mydatabase.db")
    ent=read_query(connection,get_values)
    for i in range(len(ent)):
        dt=ent[i][0]
        amount=ent[i][1]
        description=ent[i][2]
        category=ent[i][3]
        dt_lbl=tk.Label(master=fr1,text=dt)
        amount_lbl=tk.Label(master=fr1,text=amount)
        category_lbl=tk.Label(master=fr1,text=category)
        description_lbl=tk.Label(master=fr1,text=description)
        dt_lbl.grid(row=i+1,column=0)
        amount_lbl.grid(row=i+1,column=1)
        category_lbl.grid(row=i+1,column=2)
        description_lbl.grid(row=i+1,column=3)

#Method of Button '?'
def quest():
    lbl4=tk.Label(master=fr, text="DD-MM-YY", bg="white",fg="gray")
    lbl4.grid(row=2,column=1)
    lbl4.after(1800,lbl4.destroy)

#Button 'Add'
def btaddexp():
    dt=date.get()
    u=username.get()
    cat=category.get()
    desc=description.get().lower()
    n=round(abs(float(exp_ent2.get())),2)
    exp_lbl3.configure(text="")
    date.configure(text="")
    connection=create_connection("mydatabase.db")
    get_prev_exp=f"SELECT username,expense,income from login WHERE username='{u}'"
    ent=read_query(connection,get_prev_exp)
    print(ent)
    prev_exp=float(ent[0][1])
    prev_inc=float(ent[0][2])

    if ent[0][0]==u:
        #Check date is valid
        valid=True
        try:
            day,month,year=dt.split("-")
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            valid=False
        if valid:
            #Insert into 'username' table
            exp_table=f" INSERT INTO '{u}' (amount,category,date,description) VALUES ('{n}','{cat}','{dt}','{desc}') "
            execute_query(connection,exp_table)
            #Update expenses and income
            prev_exp=round(prev_exp+n,2)
            balance=prev_inc-prev_exp
            add_values=f"UPDATE login SET expense='{prev_exp}' WHERE username='{u}'"
            exp_ent2.delete(0,tk.END)
            date.delete(0,tk.END)
            description.delete(0,tk.END)
            category.set(value="")
            execute_query(connection,add_values)
            #Show 'expenses','balance'
            lbl4=tk.Label(master=fr, text=prev_exp)
            lbl4.grid(row=5,column=1)
            lbl5=tk.Label(master=fr,text=balance)
            lbl5.grid(row=8,column=1)
            if balance>=0:
                lbl5.configure(fg="green")
            else:
                lbl5.configure(fg="red")
        else:
            lbl=tk.Label(master=fr,text="Wrong date",fg="red")
            lbl.after(1800,lbl.destroy)
            lbl.grid(row=2,column=3)


def btaddinc():
    u=username.get()
    ni=round(abs(float(inc_ent1.get())),2)
    inc_lbl6.configure(text="")
    connection=create_connection("mydatabase.db")
    get_prev_inc=f"SELECT username,expense,income from login WHERE username='{u}'"
    ent=read_query(connection,get_prev_inc)
    prev_exp=round(float(ent[0][1]),2)
    prev_inc=round(float(ent[0][2]),2)
    if ent[0][0]==u:
            prev_inc=round(prev_inc+ni,2)
            balance=prev_inc-prev_exp
            add_values=f"UPDATE login SET income='{prev_inc}' WHERE username='{u}'"
            inc_ent1.delete(0,tk.END)
            execute_query(connection,add_values)
            lbl4=tk.Label(master=fr, text=prev_inc,fg="green")
            lbl4.grid(row=7, column=1)
            lbl5=tk.Label(master=fr,text=balance)
            lbl5.grid(row=8,column=1)
            if balance>=0:
                lbl5.configure(fg="green")
            else:
                lbl5.configure(fg="red")


#Welcome to your Budget App
welc=tk.Frame(master=home)
welc_lbl=tk.Label(master=welc,text="Welcome to your Budget App", font=("Cambria",44))

welc.pack()
welc_lbl.pack()


#Table 1
fr=tk.Frame(master=home)
fr.pack()
for i in range(11):
    if i<6:
        lbl=tk.Label(master=fr, text=labels[i],font=("Cambria",17))
        lbl.grid(row=i,column=0,sticky="e")
    elif i==6:
        exp_lbl3=tk.Label(master=fr,text=labels[i], fg="gray")
        exp_lbl3.grid(row=5,column=1,sticky="ew")
    elif i<9:
        lbl=tk.Label(master=fr, text=labels[i],font=("Cambria",17))
        lbl.grid(row=i-1,column=0,sticky="e")
    elif i==9:
        inc_lbl6=tk.Label(master=fr,text=labels[i], fg="gray")
        inc_lbl6.grid(row=7,column=1,sticky="ew")
    else:
        lbl=tk.Label(master=fr, text=labels[i],font=("Cambria",17))
        lbl.grid(row=8,column=0,sticky="e")

username=tk.Entry(master=fr)
exp_ent2=tk.Entry(master=fr)

inc_ent1=tk.Entry(master=fr)

category=ttk.Combobox(master=fr, values=categories, state="readonly")
date=tk.Entry(master=fr)
description=tk.Entry(master=fr)

username.grid(row=0,column=1,sticky="ew")
category.grid(row=1,column=1)
date.grid(row=2,column=1,sticky="ew")
description.grid(row=3,column=1,sticky="ew")
exp_ent2.grid(row=4,column=1,sticky="ew")
inc_ent1.grid(row=6,column=1,sticky="ew")

#Buttons
btn_addexp=tk.Button(master=fr, text="Add", borderwidth=0,command=btaddexp)
btn_addexp.grid(row=4,column=2)

btn_addinc=tk.Button(master=fr, text="Add",borderwidth=0, command=btaddinc)
btn_addinc.grid(row=6,column=2)

btn1=tk.Button(master=fr, text="?", borderwidth=0,command=quest)
btn1.grid(row=2,column=2)

btn=tk.Button(master=fr,text="See all your expenses",command=exp)
btn.grid(row=10, column=0,columnspan=1)

btn=tk.Button(master=fr,text="See expenses 2",command=exp2)
btn.grid(row=10,column=1,columnspan=1)

fr1=tk.Frame(master=home)
fr1.pack()

home.mainloop()
