import mysql.connector
from tkinter import messagebox
import io
from datetime import datetime, timedelta
import mysql.connector
import tkinter as tk
from tkcalendar import Calendar
import backend


class paymentr:
    def __init__(self,email):
        # constructor for connection
        self.con = mysql.connector.connect(
            host="localhost", user="root", password="", database="group_project_python"
        )
        self.mycursor = self.con.cursor()
        self.backend_obj=backend.Customer()
        self.backend_obj.getall(email)
        self.custmobile=self.backend_obj.custmobile
  

    def gettodaydate(self):
        sql = "select current_date"
        self.mycursor.execute(sql)
        r = self.mycursor.fetchone()
        for i in r:
            s = i
        return str(s)

    def checkdateformat(self, date):
        if date == self.gettodaydate():
            print("ok")
        else:
            print("not ok")

    def payment_reminder(self):
        isnumber = False
        while isnumber != True:
            personmobileno = input("Enter Mobile Number Of The Person : ")
            if self.backend_obj.existsmobilenumber(personmobileno) == True:
                if self.custmobile == personmobileno:
                    print("You Can't Transfer Money To You!")
                    isnumber = False
                else:
                    isnumber = True
            else:
                print("mobile number not exists")
        isamount = False
        while isamount != True:
            amount = input("Enter The Amount Which You Want To Transfer : ")
            if amount.isdigit():
                isamount = True
            else:
                print("Please Enter Valid Amount!")
                isamount = False
        amount = int(amount)
        self.select_date(personmobileno, amount)

    def getpayamount(self, personmobileno):
        query = "select payamount from customer_paymentreminder where cust_mobileno=%s and paymobileno=%s"
        val = (self.custmobile, personmobileno)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchone()
        return rs[0]

    def checkdate(self):
        today = self.gettodaydate()
        query = "select paydate,paymobileno,payamount from customer_paymentreminder where cust_mobileno=%s"
        val = (self.custmobile,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        message = ""
        for i in rs:
            if today == i[0]:
                im = f"you have to pay {i[1]}  amount :{i[2]}"
                message = message + im + "\n"
            # print("you have to pay ", z[1], " amount : ", z[2])
        if message!="":
            messagebox.showinfo("Note :", message)
            query="delete from customer_paymentreminder where cust_mobileno=%s"
            val=(self.custmobile,)
            self.mycursor.execute(query,val)
            self.con.commit()

    def get_selected_date(self, root, cal, personmobileno, amount):
        selected_date = cal.get_date()
        print("Selected Date:", selected_date)
        root.destroy()
        sql = "select paymobileno,payamount,paydate from customer_paymentreminder where cust_mobileno=%s and paymobileno=%s"
        val = (self.custmobile, personmobileno)
        self.mycursor.execute(sql, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i[2] == selected_date:
                query = "update customer_paymentreminder set payamount=%s where cust_mobileno=%s and paymobileno=%s"
                amount = self.getpayamount(personmobileno) + amount
                val = (amount, self.custmobile, personmobileno)
                self.mycursor.execute(query, val)
                self.con.commit()
                break
        else:
            query = "insert into customer_paymentreminder(cust_mobileno,paymobileno,payamount,paydate) values(%s,%s,%s,%s)"
            val = (self.custmobile, personmobileno, amount, selected_date)
            self.mycursor.execute(query, val)
            self.con.commit()

    def select_date(self, personmobileno, amount):
        root = tk.Tk()
        root.title("Date Selector")
        tomorrow_date = datetime.now() + timedelta(days=1)
        cal = Calendar(
            root, selectmode="day", date_pattern="y-mm-dd", mindate=tomorrow_date
        )
        cal.pack(pady=20, padx=20)
        select_button = tk.Button(
            root,
            text="Select Date",
            command=lambda: self.get_selected_date(root, cal, personmobileno, amount),
        )
        select_button.pack(pady=10)
        root.mainloop()
