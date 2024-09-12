import mysql.connector
import backend
import datetime
import os
import smtplib
import ssl
from email.message import EmailMessage
import time

class Transaction:
    # ------------------------------------------------------------------------------------
    # constructor use for database connectivity
    def __init__(self, email):
        # require variables
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="group_project_python",
            autocommit=True,
        )
        self.mycursor = self.con.cursor()
        self.obj_backend = backend.Customer()
        self.user_email = email
        self.obj_backend.getall(email)
        self.user_accno = self.obj_backend.custaccno
        self.cust_id = self.obj_backend.custid

    # ------------------------------------------------------------------------------------
    # Select payment method
    def make_payment(self):
        print("---------------------------------------------------------------------")
        print("1. Payment using phone number ")
        print("2. Payment using upi-id ")
        print("3. Payment using Bank transfer")
        print("4. Payment using QR code ")
        print("5. Back ")
        print("6. Exit ")
        choice = int(input("Enter Your Choice : "))
        match choice:
            case 1:
                self.payment_using_phoneno(self.user_accno)
            case 2:
                self.payment_using_upi(self.user_accno)
            case 3:
                self.payment_using_accno(self.user_accno)
            case 4:
                self.payment_using_qr(self.user_accno)
            case 5:
                return
            case 6:
                exit()
            case _:
                print("Enter Valid Choice!")

    # ------------------------------------------------------------------------------------
    def payment_using_qr(self, user_accno):
        reciver_accno = "56789123456"
        query = """select t1.cust_qr from customer_info t1
                   INNER JOIN customer_bankinfo t2 
                   ON t1.cust_id = t2.cust_id
                   WHERE t2.cust_accno = %s"""
        val = (reciver_accno,)
        self.mycursor.execute(query, val)
        img_data = self.mycursor.fetchone()[0]
        file = "qr.jpeg"
        f = open(file, "wb")
        f.write(img_data)
        f.close()
        # Open the image with the default image viewer
        os.startfile(file)
        # Wait for 3 seconds before closing the image
        time.sleep(3)
        # Close the image by terminating the associated process
        os.system("taskkill /f /im mspaint.exe")
        # ask amount here
        os.remove(file)
        amount = self.take_amount()
        self.set_updates(user_accno, reciver_accno, amount)

    # ------------------------------------------------------------------------------------
    # payemnt using upi-id
    def payment_using_upi(self, user_accno):
        upi_id = self.take_upiid()
        sql = "SELECT count(*) FROM customer_info where cust_upiid = %s"
        val = (upi_id,)
        self.mycursor.execute(sql, val)
        count = self.mycursor.fetchone()[0]
        if count == 1:
            while True:
                amount = self.take_amount()
                current_balance = self.get_balance(user_accno)
                if current_balance >= amount:
                    pin = input("Enter pin to confirm payment :")
                    sql = """SELECT t1.upi_pin FROM customer_info t1
                            INNER JOIN customer_bankinfo t2 ON t1.cust_id = t2.cust_id
                            WHERE t2.cust_accno = %s """
                    val = (user_accno,)
                    self.mycursor.execute(sql, val)
                    cust_pin = self.mycursor.fetchone()[0]
                    if cust_pin == pin:
                        sql = """SELECT t1.cust_accno
                            FROM customer_bankinfo t1
                            INNER JOIN customer_info t2 ON t1.cust_id = t2.cust_id
                            WHERE t2.cust_upiid = %s """
                        val = (upi_id,)
                        self.mycursor.execute(sql, val)
                        reciver_accno = self.mycursor.fetchone()[0]
                        self.set_updates(user_accno, reciver_accno, amount)
                        break
                    else:
                        print("Wrong pin")
                else:
                    print("Insufficient balance")
        else:
            print("Please enter valid details")

    def take_upiid(self):
        upiid = input("Enter upi-id : ")
        if self.check_existancy("cust_upiid", upiid):
            return upiid
        else:
            print("Please enter valid upi-id")
            return self.take_upiid()

    def check_existancy(self, column_name, data):
        query = "Select count(*) from customer_info where " + column_name + " = %s"
        val = (data,)
        self.mycursor.execute(query, val)
        count = self.mycursor.fetchone()[0]
        if count == 1:
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------
    # payemnt using Phone no.
    def payment_using_phoneno(self, user_accno):
        phone_no = self.take_phoneno()
        sql = "SELECT count(*) FROM customer_info where cust_mobileno = %s"
        val = (phone_no,)
        self.mycursor.execute(sql, val)
        count = self.mycursor.fetchone()[0]
        if count == 1:
            while True:
                amount = self.take_amount()
                current_balance = self.get_balance(user_accno)
                if current_balance >= amount:
                    pin = input("Enter pin to confirm payment :")
                    sql = """SELECT t1.upi_pin FROM customer_info t1
                            INNER JOIN customer_bankinfo t2 ON t1.cust_id = t2.cust_id
                            WHERE t2.cust_accno = %s """
                    val = (user_accno,)
                    self.mycursor.execute(sql, val)
                    cust_pin = self.mycursor.fetchone()[0]
                    if cust_pin == pin:
                        sql = """SELECT t1.cust_accno
                                FROM customer_bankinfo t1
                                INNER JOIN customer_info t2 ON t1.cust_id = t2.cust_id
                                WHERE t2.cust_mobileno = %s """
                        val = (phone_no,)
                        self.mycursor.execute(sql, val)
                        reciver_accno = self.mycursor.fetchone()[0]
                        self.set_updates(user_accno, reciver_accno, amount)
                        break
                    else:
                        print("Wrong pin")
                else:
                    print("Insufficient balance")
        else:
            print("Please enter valid Phone no.")

    def take_phoneno(self):
        phone_no = input("Enter phone no. : ")
        if len(phone_no) == 10:
            if phone_no.isdigit():
                if self.check_existancy("cust_mobileno", phone_no):
                    return phone_no
                else:
                    print("Please enter valid phone no.")
                    return self.take_phoneno()
            else:
                print("Phone number conatins only digits.Please Enter valid phone no.")
                return self.take_phoneno()
        else:
            print(
                "Phone number's length must br 10 digits.Please Enter valid phone no."
            )
            return self.take_phoneno()

    # ------------------------------------------------------------------------------------
    # payemnt using account no.
    def payment_using_accno(self, user_accno):
        reciver_accno = self.take_accno()
        ifsc_code = input("Enter IFSC code : ")
        sql = "SELECT count(*) FROM customer_bankinfo where cust_accno = %s and cust_ifsc = %s"
        val = (reciver_accno, ifsc_code)
        self.mycursor.execute(sql, val)
        count = self.mycursor.fetchone()[0]
        if count == 1:
            amount = self.take_amount()
            current_balance = self.get_balance(user_accno)
            if current_balance >= amount:
                pin = input("Enter pin to confirm payment :")
                sql = """SELECT t1.upi_pin FROM customer_info t1
                        INNER JOIN customer_bankinfo t2 ON t1.cust_id = t2.cust_id
                        WHERE t2.cust_accno = %s """
                val = (user_accno,)
                self.mycursor.execute(sql, val)
                cust_pin = self.mycursor.fetchone()[0]
                while True:
                    if cust_pin == pin:
                        self.set_updates(user_accno, reciver_accno, amount)
                        break
                    else:
                        print("Wrong pin")
            else:
                print("Insufficient balance")
        else:
            print("Please enter valid details")

    def take_accno(self):
        reciver_accno = input("Enter Account no. : ")
        if reciver_accno.isdigit():
            query = "Select count(*) from customer_bankinfo where cust_accno = %s"
            val = (reciver_accno,)
            self.mycursor.execute(query, val)
            count = self.mycursor.fetchone()[0]
            if count == 1:
                return reciver_accno
            else:
                print("Please enter valid Account no.")
                return self.take_accno()
        else:
            print("Account no. conatins only digits.Please Enter valid phone no.")

    # ------------------------------------------------------------------------------------
    # get amount from user
    def take_amount(self):
        amount = input("Enter amount : ")
        try:
            amount = float(amount)
            if amount > 100000.0:
                print("limit is less than 100000")
                return self.take_amount()
            else:
                return amount
        except:
            print("Enter valid amount !! ")
            return self.take_amount()

    # ------------------------------------------------------------------------------------
    # set new values in database
    def set_updates(self, user_accno, reciver_accno, amount):
        debit_massage = (amount, "rupees debited from your account")
        self.obj_backend.speak(debit_massage)
        self.update_balance(user_accno, amount, "debit")
        self.set_cust_spend(user_accno, amount)
        self.add_history(user_accno, amount, "debit")
        self.increase_no_of_payment(user_accno)
        self.obj_backend.getrewards(self.user_email, user_accno)
        # reciver
        self.update_balance(reciver_accno, amount, "credit")
        self.set_cust_recived(reciver_accno, amount)
        self.add_history(reciver_accno, amount, "credit")

    def fatch_no_of_transaction(self, user_accno):
        sql = """SELECT t1.no_of_transaction from customer_transaction t1 
                INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s"""
        val = (user_accno,)
        self.mycursor.execute(sql, val)
        no_of_transactions = self.mycursor.fetchone()[0]
        return no_of_transactions

    def increase_no_of_payment(self, user_accno):
        no_of_transactions = self.fatch_no_of_transaction(user_accno)
        sql = """Update customer_transaction set no_of_transaction = %s 
                WHERE cust_id = (SELECT cust_id FROM customer_bankinfo
                WHERE cust_accno = %s)"""
        val = (no_of_transactions + 1, user_accno)
        self.mycursor.execute(sql, val)

    # ------------------------------------------------------------------------------------
    # balance update operation
    def update_balance(self, acc_no, amount, tran_type):
        balance = self.get_balance(acc_no)
        if tran_type == "credit":
            balance += amount
            self.set_balance(acc_no, balance)
        elif tran_type == "debit":
            balance -= amount
            self.set_balance(balance, acc_no)

    # get current balance of account
    def get_balance(self, acc_no):
        sql = "SELECT cust_balance FROM customer_bankinfo where cust_accno = %s"
        val = (acc_no,)
        self.mycursor.execute(sql, val)
        balance = self.mycursor.fetchone()[0]
        return balance

    # set new balance after credit or debit
    def set_balance(self, acc_no, balance):
        sql = "UPDATE customer_bankinfo SET cust_balance = %s WHERE cust_accno = %s"
        val = (balance, acc_no)
        self.mycursor.execute(sql, val)

    # ------------------------------------------------------------------------------------
    # get total cust_spend amount from customer_transaction table
    def get_cust_spend(self, cust_accno):
        sql = """SELECT cust_spent from customer_transaction t1
                INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s"""
        val = (cust_accno,)
        self.mycursor.execute(sql, val)
        cust_spend = self.mycursor.fetchone()[0]
        return cust_spend

    # get total cust_reciveed amount from customer_transaction table
    def get_cust_recived(self, cust_accno):
        sql = """SELECT cust_recived from customer_transaction t1
                INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s"""
        val = (cust_accno,)
        self.mycursor.execute(sql, val)
        cust_recived = self.mycursor.fetchone()[0]
        return cust_recived

    # set total cust_spend amount in customer_transaction table after transaction
    def set_cust_spend(self, cust_accno, amount):
        cust_spend = self.get_cust_spend(cust_accno)
        cust_spend = cust_spend + amount
        sql = """UPDATE customer_transaction t1 INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                SET t1.cust_spent = %s WHERE t2.cust_accno = %s """
        val = (cust_spend, cust_accno)
        self.mycursor.execute(sql, val)

    # set total cust_recived amount in customer_transaction table after transaction
    def set_cust_recived(self, cust_accno, amount):
        cust_recived = self.get_cust_recived(cust_accno)
        cust_recived = cust_recived + amount
        sql = """UPDATE customer_transaction t1 INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                SET t1.cust_recived = %s WHERE t2.cust_accno  = %s """
        val = (cust_recived, cust_accno)
        self.mycursor.execute(sql, val)

    # ----------------------------------------------------------------------------------------
    # add rows in history table when payment done
    def add_history(self, acc_no, amount, tran_type):
        sql = """SELECT transaction_history from customer_transaction t1
                INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s"""
        val = (acc_no,)
        self.mycursor.execute(sql, val)
        old_content = self.mycursor.fetchone()[0]
        f1 = open("history.txt", "w+")

        row = f"{self.current_date():^15}|{self.current_time():^15}|{acc_no:^17}|{amount:^14}|{tran_type:^14}"
        f1.write(old_content.decode() + "\n")
        f1.write(row)
        f1.seek(0)
        content = f1.read()
        f1.close()
        os.remove("history.txt")
        sql = """UPDATE customer_transaction t1 INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                SET t1.transaction_history = %s WHERE t2.cust_accno  = %s """
        val = (content, acc_no)
        self.mycursor.execute(sql, val)

    # get current date
    def current_date(self):
        current_date = datetime.date.today()
        current_date = current_date.strftime("%d-%m-%Y")
        return current_date

    # get current time
    def current_time(self):
        current_time = datetime.datetime.now().time()
        current_time = current_time.strftime("%H:%M:%S")
        return current_time

    # ----------------------------------------------------------------------------------
    # call this method at login time to write details of user and column names into file
    def create_tran_history_file(self, cust_id, acc_holder_name, acc_no):
        query = "INSERT INTO customer_transaction(cust_id,transaction_history,cust_spent,cust_recived) VALUES(%s,%s,%s,%s)"
        val = (cust_id, self.set_data(acc_holder_name, acc_no), 0, 0)
        self.mycursor.execute(query, val)

    def set_data(self, acc_holder_name, acc_no):
        file_name = "history.txt"
        f1 = open(file_name, "a+")
        f1.write("Account holder name : " + acc_holder_name + "\n")
        f1.write("Account number : " + acc_no + "\n\n")
        f1.write(
            "     Date      |      Time     |   Account no.   |    amount    |   tran_type \n"
        )
        f1.write(
            "---------------+---------------+-----------------+--------------+-------------\n"
        )
        f1.seek(0)
        content = f1.read()
        f1.close()
        os.remove(file_name)
        return content.encode()

    # ----------------------------------------------------------------------------------
    # call this method to open history file
    def print_history(self):
        query = """SELECT transaction_history from customer_transaction t1
                INNER JOIN customer_bankinfo t2 
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s"""
        val = (self.user_accno,)
        self.mycursor.execute(query, val)
        content = self.mycursor.fetchone()[0]
        f1 = open("history.txt", "wb")
        f1.write(content)
        f1.write(b"\n\n\n")
        f1.write(
            (
                "Total spend : " + str(self.get_cust_spend(self.user_accno)) + "\n"
            ).encode()
        )
        f1.write(
            ("Total recived : " + str(self.get_cust_recived(self.user_accno))).encode()
        )
        f1.close()
        os.startfile("history.txt")

    def send_opt(self, user_email_id, otp):
        # Define email sender and receiver
        email_sender = "dummmmymaill7878@gmail.com"
        email_password = "oabi jtji kuoi gefr"
        email_receiver = user_email_id
        # Set the subject and body of the email
        subject = "Check out my new video!"
        body = f"""
        yout OTP is {otp} ."""

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def pay_amount(self, reciver_accno, amount):
        amount = self.take_amount()
        pin = input("Enter pin to confirm payment :")
        sql = """SELECT t1.upi_pin FROM customer_info t1
                INNER JOIN customer_bankinfo t2 ON t1.cust_id = t2.cust_id
                WHERE t2.cust_accno = %s """
        val = (self.user_accno,)
        self.mycursor.execute(sql, val)
        cust_pin = self.mycursor.fetchone()[0]
        if cust_pin == pin:
            current_balance = self.get_balance(self.user_accno)
            if current_balance >= amount:
                self.set_updates(self.user_accno, reciver_accno, amount)
            else:
                print("Insufficient balance")
        else:
            print("Wrong pin")


""" tran=Transaction("archanpatel7233@gmail.com") """




