import tkinter as tk
from tkinter import ttk
import datetime

from database_methods import create_connection, execute_query, read_query

#Lists
labels=["Username: ","Category: ","Date: ","Description: ", "Enter your expenses here: ",
 "You have spent: ","Please enter a number above","Enter your income here: ",
  "Total income: ", "Please enter a number above","Balance: "]

categories=["Clothing","Entertainment", "Groceries", "Rent", "Transport/Travel","Other"]

names=["Date","Amount","Description","Category"]

class App(tk.Frame):
    def __init__(self,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
    def show(self):
        self.lift()

class Home(App):
    def __init__(self,*args,**kwargs):
        App.__init__(self,*args,*kwargs)
        bt1=tk.Button(self, text="Clothing")
        bt2=tk.Button(self,text="Entertainment")
        bt3=tk.Button(self, text="Groceries")
        bt4=tk.Button(self,text="Rent")
        bt5=tk.Button(self,text="Transport/Travel")
        bt6=tk.Button(self,text="Other")
        bt1.pack(fill="both", expand=True)
        bt2.pack(fill="both", expand=True)
        bt3.pack(fill="both", expand=True)
        bt4.pack(fill="both", expand=True)
        bt5.pack(fill="both", expand=True)
        bt6.pack(fill="both", expand=True)

class Addexp(App):
   def __init__(self, *args, **kwargs):
       App.__init__(self, *args, **kwargs)

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
                   lbl4=tk.Label(self, text=prev_exp)
                   lbl4.grid(row=5,column=1)
                   lbl5=tk.Label(self,text=balance)
                   lbl5.grid(row=8,column=1)
                   if balance>=0:
                       lbl5.configure(fg="green")
                   else:
                       lbl5.configure(fg="red")
               else:
                   lbl=tk.Label(self,text="Wrong date",fg="red")
                   lbl.after(1800,lbl.destroy)
                   lbl.grid(row=2,column=3)

        # Button for Adding income
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
                    lbl4=tk.Label(self, text=prev_inc,fg="green")
                    lbl4.grid(row=7, column=1)
                    lbl5=tk.Label(self,text=balance)
                    lbl5.grid(row=8,column=1)
                    if balance>=0:
                        lbl5.configure(fg="green")
                    else:
                        lbl5.configure(fg="red")


       #Table 1
       for i in range(11):
           if i<6:
               lbl=tk.Label(self, text=labels[i],font=("Cambria",17))
               lbl.grid(row=i,column=0,sticky="e")
           elif i==6:
               exp_lbl3=tk.Label(self,text=labels[i], fg="gray")
               exp_lbl3.grid(row=5,column=1,sticky="ew")
           elif i<9:
               lbl=tk.Label(self, text=labels[i],font=("Cambria",17))
               lbl.grid(row=i-1,column=0,sticky="e")
           elif i==9:
               inc_lbl6=tk.Label(self,text=labels[i], fg="gray")
               inc_lbl6.grid(row=7,column=1,sticky="ew")
           else:
               lbl=tk.Label(self, text=labels[i],font=("Cambria",17))
               lbl.grid(row=8,column=0,sticky="e")

       username=tk.Entry(self)
       exp_ent2=tk.Entry(self)

       inc_ent1=tk.Entry(self)

       category=ttk.Combobox(self, values=categories, state="readonly")
       date=tk.Entry(self)
       description=tk.Entry(self)

       username.grid(row=0,column=1,sticky="ew")
       category.grid(row=1,column=1)
       date.grid(row=2,column=1,sticky="ew")
       description.grid(row=3,column=1,sticky="ew")
       exp_ent2.grid(row=4,column=1,sticky="ew")
       inc_ent1.grid(row=6,column=1,sticky="ew")

      #Buttons
       btn_addexp=tk.Button(self, text="Add", borderwidth=0,command=btaddexp)
       btn_addexp.grid(row=4,column=2)

       btn_addinc=tk.Button(self, text="Add",borderwidth=0)
       btn_addinc.grid(row=6,column=2)

       btn1=tk.Button(self, text="?", borderwidth=0)
       btn1.grid(row=2,column=2)


class Account(App):
   def __init__(self, *args, **kwargs):
       App.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="T")
       label.pack(side="top", fill="both", expand=True)

class View_exp(App):
    def __init__(self,*args,**kwargs):
        App.__init__(self,*args,**kwargs)
        def exp():
            u=username.get()
            for i in range(4):
                label=tk.Label(self,text=names[i],width=10)
                label.grid(row=1,column=i,sticky="ew")

            get_values=f"SELECT date,amount,category,description from '{u}'"
            connection=create_connection("mydatabase.db")
            ent=read_query(connection,get_values)
            for i in range(len(ent)):
                dt=ent[i][0]
                amount=ent[i][1]
                description=ent[i][2]
                category=ent[i][3]
                dt_lbl=tk.Label(self,text=dt)
                amount_lbl=tk.Label(self,text=amount)
                category_lbl=tk.Label(self,text=category)
                description_lbl=tk.Label(self,text=description)
                dt_lbl.grid(row=i+2,column=0)
                amount_lbl.grid(row=i+2,column=1)
                category_lbl.grid(row=i+2,column=2)
                description_lbl.grid(row=i+2,column=3)

        username_label=tk.Label(self,text="Username: ")
        username=tk.Entry(self)
        btn=tk.Button(self,text="See expenses",command=exp)
        username_label.grid(row=0,column=0)
        username.grid(row=0,column=1)
        btn.grid(row=0,column=2)

class Homepageview(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        home = Home(self)
        addexp = Addexp(self)
        account = Account(self)
        view_exp = View_exp(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        container2=tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        home.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        addexp.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        account.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        view_exp.place(in_=container,x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Home", command=home.show)
        b2 = tk.Button(buttonframe, text="Add your expenses", command=addexp.show)
        b3 = tk.Button(buttonframe, text="My Account", command=account.show)
        b4 = tk.Button(buttonframe,text="See your expenses", command=view_exp.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        home.show()

if __name__ == "__main__":
    window = tk.Tk()
    main = Homepageview(window)
    main.pack(side="top", fill="both", expand=True)
    window.wm_geometry("600x500")
    window.title("BudgetApp")
    window.mainloop()
