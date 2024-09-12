from tkinter import messagebox
import random
import mysql.connector


def getrewards(id):
    con = mysql.connector.connect(
        host="localhost", user="root", password="", database="group_project_python"
    )
    mycursor = con.cursor()
    query = "select no_of_transaction from customer_transaction where cust_id=%s"
    val = (id,)
    mycursor.execute(query, val)
    rs = mycursor.fetchone()
    no_of_transaction=rs[0]
    if no_of_transaction % 5 == 0 and no_of_transaction % 10 != 0:
        reward = random.randint(1, 100)
        sentence = f"You Got : {reward} Rupees"
        messagebox.showinfo("Note :", sentence)
    elif no_of_transaction % 5 == 0 and no_of_transaction % 10 == 0:
        reward = random.randint(100, 200)
        sentence = f"You Got : {reward} Rupees"
        messagebox.showinfo("Note :", sentence)