import qrcode
import uuid
from tkinter import messagebox
import io
from datetime import datetime, timedelta
import mysql.connector
import random
from tkinter import filedialog
import tkinter as tk
from tkcalendar import Calendar
import Transaction as tran
import pyttsx3
import paymentreminder as pr


class Customer:
    def __init__(self):
        # constructor for connection
        self.con = mysql.connector.connect(
            host="localhost", user="root", password="", database="group_project_python"
        )
        self.mycursor = self.con.cursor()

    def closecon(self):
        # for close the connection
        self.mycursor.close()
        self.con.close()

    def getid(self, email):
        # for get id of particular person
        sql = "select cust_id from customer_info where cust_email=%s"
        val = (email,)
        self.mycursor.execute(sql, val)
        cust_id = self.mycursor.fetchone()[0]
        return cust_id

    def getall(self, email):
        # for get customer id,mobile number,account number and upi-id of particular person
        sql = "select customer_info.cust_id,customer_info.cust_mobileno,customer_info.cust_upiid,customer_bankinfo.cust_accno from customer_info inner join customer_bankinfo on customer_info.cust_id=customer_bankinfo.cust_id where customer_info.cust_email=%s"
        val = (email,)
        self.mycursor.execute(sql, val)
        data = self.mycursor.fetchone()
        self.custid = data[0]
        self.custmobile = data[1]
        self.custupiid = data[2]
        self.custaccno = data[3]

    def checkpassword(self, password=""):
        # for check the password is strong or not
        # conditions:must have at-least one digit,lower and upper case letter and one special character and length should be greater than 7
        ispasword = False
        count = 0
        upper1 = 0
        lower1 = 0
        special1 = 0
        dig1 = 0
        if len(password) >= 8:
            for i in password:
                if i.isupper():
                    count += 1
                    upper1 = 1
                elif i.islower():
                    count += 1
                    lower1 = 1
                elif i.isdigit():
                    count += 1
                    dig1 = 1
                elif (
                    i == "@"
                    or i == "#"
                    or i == "&"
                    or i == "$"
                    or i == "%"
                    or i == "!"
                    or i == "^"
                    or i == "*"
                ):
                    count += 1
                    special1 = 1
            if (
                count >= 4
                and upper1 == 1
                and lower1 == 1
                and dig1 == 1
                and special1 == 1
            ):
                ispasword = True
            else:
                ispasword = False
                if dig1 == 0:
                    print("Your Password Doesn't Contains Digit!")
                if special1 == 0:
                    print(
                        "Your Password Doesn't Contains Special Character Just Like @,#,etc..!"
                    )
                if upper1 == 0:
                    print("Your Password Doesn't Contains UpperCase Letter!")
                if lower1 == 0:
                    print("Your Password Doesn't Contains LowerCase Letter!")
        else:
            print("Your Password Length Must Be Greater Or Equal To 8!")
            ispasword = False
        return ispasword

    def take_emailid(self):
        isemail = False
        while isemail != True:
            cust_email = input("Enter Your E-mail ID : ")
            if self.checkemail(cust_email) == False:
                if (
                    cust_email.endswith("@gmail.com")
                    or cust_email.endswith("@yahoo.com")
                    or cust_email.endswith("@icloud.com")
                    or cust_email.endswith("@outlook.com")
                ):
                    isemail = True
                    return cust_email
                else:
                    isemail = False
                    print("Your E-mail ID is Not Valid!")
            else:
                isemail = False
                print("E-mail ID Is Already Exists!")

    def take_password(self):
        s = """password length must be greater or equal to 8 and
password must contain one digit,lowercase,uppercase
and one special symbol"""
        print(s)
        ispasscode = False
        while ispasscode != True:
            passw = input("Enter Your Password : ")
            passw = passw.strip(" ")
            if self.checkpassword(passw) == True:
                ispasscode = True
                return passw
            else:
                ispasscode = False

    def take_name(self):
        isname = False
        while isname != True:
            name = input("Enter Your Name : ")
            for i in name:
                if i.isalpha() or i == " ":
                    isname = True
                    return name
                else:
                    print("Please Enter Valid Name!")
                    isname = False
                    break
        name = name.strip(" ")

    def take_phone_no(self):
        ismobile = False
        while ismobile != True:
            mobilenumber = input("Enter Your Mobile Number : ")
            mobilenumber = mobilenumber.strip(" ")
            if len(mobilenumber) == 10:
                if mobilenumber.isdigit():
                    if self.existsmobilenumber(mobilenumber) == False:
                        if (
                            mobilenumber.startswith("9")
                            or mobilenumber.startswith("8")
                            or mobilenumber.startswith("7")
                            or mobilenumber.startswith("6")
                        ):
                            ismobile = True
                            return mobilenumber
                        else:
                            ismobile = False
                            print("Invalid MobileNumber!")
                    else:
                        print("MobileNumber Already Registered")
                else:
                    ismobile = False
                    print("Invalid MobileNumber!")
            else:
                ismobile = False
                print("Invalid Mobilenumber")

    def take_accno(self):
        isaccno = False
        while isaccno != True:
            accno = input("Enter Your Account Number : ")
            if self.existsaccno(accno) == False:
                if len(accno) == 11 and accno.isdigit():
                    isaccno = True
                    return accno
                else:
                    print("Enter valid account number")
                    isaccno = False
            else:
                print("account number already exists")
                isaccno = False

    def take_ifsc_code(self):
        isifsc = False
        while isifsc != True:
            ifsc = input("Enter Your IFSC Code : ")
            count1 = 0
            count2 = 0
            for i in ifsc:
                if i.isalpha():
                    count1 = 1
                elif i.isdigit():
                    count2 = 1
            if count1 == 1 and count2 == 1:
                isifsc = True
                return ifsc
            else:
                isifsc = False
                print("Enter Valid IFSC Code!")

    def take_bank_name(self):
        isbank = False
        while isbank != True:
            bankname = input("Enter Your Bank Name : ")
            if bankname.isalpha():
                isbank = True
                return bankname
            else:
                print("Enter valid bank name")
                isbank = False
        bankname = bankname.strip(" ")

    def take_upipin(self):
        ispin = False
        while ispin != True:
            pin = input("Enter Your Pin : ")
            if len(pin) == 6:
                if pin.isdigit():
                    print("Your Pin Is Set!")
                    ispin = True
                    return pin
                else:
                    ispin = False
                    print("Enter Valid Pin!")
            else:
                ispin = False
                print("Pin Length Must be 6!")

    def customer_signup(self):
        # signup method
        self.cust_email = self.take_emailid()
        self.cust_pass = self.take_password()
        self.cust_name = self.take_name()
        self.cust_phoneno = self.take_phone_no()
        self.cust_accno = self.take_accno()
        ifsc = self.take_ifsc_code()
        bank_name = self.take_bank_name()
        # make upi-id
        self.cust_upiid = self.cust_accno + "@ok" + bank_name
        # genrate upipin
        pin = self.take_upipin()
        query = "INSERT INTO customer_info(cust_email,cust_password,cust_mobileno,cust_name,cust_qr,cust_upiid,upi_pin) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        qrc = self.generate_qrcode()
        val = (
            self.cust_email,
            self.cust_pass,
            self.cust_phoneno,
            self.cust_name,
            qrc,
            self.cust_upiid,
            pin,
        )
        self.mycursor.execute(query, val)
        self.con.commit()
        query = "INSERT INTO customer_bankinfo(cust_id,cust_accno,cust_ifsc,cust_balance) VALUES(%s,%s,%s,%s)"
        self.cust_id = self.getid(self.cust_email)
        bal = 50000
        val = (self.cust_id, self.cust_accno, ifsc, bal)
        self.mycursor.execute(query, val)
        self.con.commit()
        self.getall(self.cust_email)
        tran_hist = tran.Transaction(self.cust_email)
        tran_hist.create_tran_history_file(
            self.cust_id, self.cust_name, self.cust_accno
        )
        print("Sign-Up SuccessFully!")
        paymentreminder_obj = pr.paymentr(self.cust_email)
        paymentreminder_obj.checkdate()

    def cust_login(self):
        islogin = False
        isemail = False
        while isemail != True:
            self.cust_email = input("Enter Your E-mail : ").lower().strip()
            if self.checkemail(self.cust_email) == True:
                ispass = False
                while ispass != True:
                    passc = input("Enter Your Password : ").strip()
                    if self.checkemailpass(self.cust_email, passc) == True:
                        print("SuccesFully Login!")
                        paymentreminder_obj = pr.paymentr(self.cust_email)
                        paymentreminder_obj.checkdate()
                        ispass = isemail = True
                    else:
                        ispass = isemail = False
                        print("Enter Valid Password!")
                        answer = input("Did You Forgot Your Password?")
                        if answer.lower() == "yes":
                            isnumber = False
                            while isnumber != True:
                                number = input("Enter Your Registered MobileNumber : ")
                                if self.existsmobilenumberlogin(
                                    number, self.cust_email
                                ):
                                    isotp = False
                                    while isotp != True:
                                        genrated_otp = random.randrange(1000, 10000)
                                        tran_obj = tran.Transaction(self.cust_email)
                                        tran_obj.send_opt(self.cust_email, genrated_otp)
                                        print("your otp is : ", genrated_otp)
                                        otp = input("Enter The OTP : ")
                                        if otp.isdigit():
                                            otp = int(otp)
                                            if otp == genrated_otp:
                                                isotp = isnumber = True
                                            else:
                                                isotp = False
                                        else:
                                            print("Please Enter Valid OTP!")
                                            isotp = False
                                else:
                                    print("Please Enter Valid Number!")
                                    isnumber = False
                            isnewp = False
                            while isnewp != True:
                                newp = input("Enter Your New Password : ")
                                if self.checkpassword(newp) == True:
                                    self.forgotpass(self.cust_email, newp)
                                    print("Login SuccessFully!")
                                    paymentreminder_obj = pr.paymentr(self.cust_email)
                                    paymentreminder_obj.checkdate()
                                    isnewp = ispass = isemail = True
                                else:
                                    isnewp = ispass = isemail = False
            else:
                print("Enter Valid E-mail!")
        islogin = True
        return islogin

    def existsmobilenumberlogin(self, number, email):
        isnumber = False
        query = "select * from customer_info where cust_mobileno=%s and cust_email=%s"
        val = (number, email)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i != "":
                isnumber = True
        return isnumber

    def generate_qrcode(self):
        data = str(uuid.uuid4())
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_bytes = buffered.getvalue()

        # Check if the generated QR code already exists in the database
        sql = "SELECT cust_qr FROM customer_info"
        self.mycursor.execute(sql)
        qr_all = self.mycursor.fetchall()
        for qr_data in qr_all:
            if (
                qr_code_bytes in qr_data
            ):  # Comparing bytes directly won't work as expected
                return self.generate_qrcode()  # If QR code exists, regenerate
        return qr_code_bytes  # If QR code doesn't exist, return the generated bytes

    def forgotpass(self, email, newpassc):
        query = "update customer_info set cust_password=%s where cust_email=%s"
        val = (newpassc, email)
        self.mycursor.execute(query, val)
        self.con.commit()

    def checkemail(self, email):
        isemail = False
        query = "select * from customer_info where cust_email=%s"
        val = (email,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i != "":
                isemail = True
        return isemail

    def checkemailpass(self, email, pasc):
        islogin = False
        query = "select * from customer_info where cust_email=%s and cust_password=%s"
        val = (email, pasc)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i != "":
                islogin = True
        return islogin

    def existsmobilenumber(self, number):
        isnumber = False
        query = "select * from customer_info where cust_mobileno=%s"
        val = (number,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i != "":
                isnumber = True
        return isnumber

    def existsaccno(self, accno):
        isaccno = False
        query = "select * from customer_bankinfo where cust_accno=%s"
        val = (accno,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if i != "":
                isaccno = True
        return isaccno

    def speak(self, massage, rate=150):
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", rate)
        engine.say(massage, "Transaction massage")
        engine.runAndWait()

    def checkalpha(self, inpt):
        isinput = False
        while isinput != True:
            alph = input(inpt)
            if alph.isalpha():
                isinput = True
            else:
                print()
                print("|----------------------------|")
                print("| Please Enter Valid Detail! |")
                print("|----------------------------|")
                print()
                isinput = False
        return alph

    def checkdigit(self, inpt):
        isinput = False
        while isinput != True:
            dig = input(inpt)
            if dig.isdigit():
                isinput = True
            else:
                isinput = False
                print()
                print("|----------------------------|")
                print("| Please Enter Valid Detail! |")
                print("|----------------------------|")
                print()
        return dig

    def checkalphadig(self, inpt):
        isinput = False
        while isinput != True:
            digalph = input(inpt)
            if digalph.isalnum():
                isinput = True
            else:
                isinput = False
                print()
                print("|----------------------------|")
                print("| Please Enter Valid Detail! |")
                print("|----------------------------|")
                print()
        return digalph

    def checkalphadigcomp(self, inpt):
        isinput = False
        while isinput != True:
            digalph = input(inpt)
            count1 = count2 = 0
            for i in digalph:
                if i.isdigit():
                    count1 = 1
                elif i.isalpha():
                    count2 = 1
                else:
                    count1 = count2 = 0
            if count1 == 1 and count2 == 1:
                isinput = True
            else:
                isinput = False
                print()
                print("|----------------------------|")
                print("| Please Enter Valid Detail! |")
                print("|----------------------------|")
                print()
        return digalph

    def isfloat(self, statement):
        isnumber = False
        while isnumber != True:
            number = input(statement)
            count = 0
            count1 = 0
            for i in number:
                if i.isdigit():
                    count += 1
                elif i == "." and count > 0:
                    count1 += 1
            if count == len(number) - 1 and count1 == 1:
                isnumber = True
            elif count == len(number) and count1 == 0:
                isnumber = True
            else:
                print()
                print("|----------------------------|")
                print("| Please Enter Valid Detail! |")
                print("|----------------------------|")
                print()
                isnumber = False
        return number

    def getrewards(self, cust_email, cust_accno):
        query = """select no_of_transaction from customer_transaction t1
                INNER JOIN customer_info t2
                ON t1.cust_id = t2.cust_id
                WHERE t2.cust_email = %s"""
        val = (cust_email,)
        self.mycursor.execute(query, val)
        no_of_transaction = self.mycursor.fetchone()[0]
        transaction_obj = tran.Transaction(cust_email)
        if no_of_transaction % 5 == 0 and no_of_transaction % 10 != 0:
            reward = random.randint(1, 100)
            reward = float(reward)
            sentence = f"You Got : {reward} Rupees"
            messagebox.showinfo("Note :", sentence)
            transaction_obj.update_balance(cust_accno, reward, "credit")
        elif no_of_transaction % 5 == 0 and no_of_transaction % 10 == 0:
            reward = random.randint(100, 200)
            reward = float(reward)
            sentence = f"You Got : {reward} Rupees"
            messagebox.showinfo("Note :", sentence)
            transaction_obj.update_balance(cust_accno, reward, "credit")
