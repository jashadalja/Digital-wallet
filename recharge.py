import datetime
from datetime import timedelta, date
import Transaction as tran
import mysql.connector
import backend as back
import os
import random


class Recharge:
    def __init__(self, email):
        self.con = mysql.connector.connect(
            host="localhost", user="root", password="", database="group_project_python"
        )
        self.mycursor = self.con.cursor()
        backend_obj = back.Customer()
        self.transaction_obj = tran.Transaction(email)
        backend_obj.getall(email)
        self.custid = backend_obj.custid
        self.custaccno = backend_obj.custaccno
        self.custmobile = backend_obj.custmobile
        self.custbalance = self.transaction_obj.get_balance(self.custaccno)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # to fetch current plan and validity from database
    def display_menu(self):
        self.get_current_plan()
        while True:
            print("\n")
            print(
                " -------------------------------------------------------------------------------"
            )
            print(
                "| 1) Recharge                                                                   |"
            )
            print(
                " -------------------------------------------------------------------------------"
            )
            print(
                "| 2) Current plan                                                               |"
            )
            print(
                " -------------------------------------------------------------------------------"
            )
            print(
                "| 3) Recharge history                                                           |"
            )
            print(
                " -------------------------------------------------------------------------------"
            )
            print(
                "| 4) Exit                                                                       |"
            )
            print(
                " -------------------------------------------------------------------------------"
            )
            choice = input("Enter your choice: ")
            if choice == "1":

                # -------------------------------------------------------------------------------------------------------------------------------
                # will only let you recharge if current plan has expired
                curr_plan_details = self.get_current_plan()
                valid_till = curr_plan_details[1]
                if valid_till < date.today():
                    print("\n")
                    print(
                        " -------------------------------------------------------------------------------"
                    )
                    print(
                        "| 1) Recharge for Jio                                                           |"
                    )
                    print(
                        " -------------------------------------------------------------------------------"
                    )
                    print(
                        "| 2) Recharge for Airtel                                                        |"
                    )
                    print(
                        " -------------------------------------------------------------------------------"
                    )
                    print(
                        "| 3) Recharge for Vi                                                            |"
                    )
                    print(
                        " -------------------------------------------------------------------------------"
                    )
                    choice = input("")
                    if choice == "1":
                        self.jio_plans()
                    elif choice == "2":
                        self.airtel_plans()
                    elif choice == "3":
                        self.vi_plans()
                    else:
                        print("\nInvalid input")
                else:
                    print(
                        "\nUnable to recharge at the moment. Try checking your current recharge plan."
                    )
            elif choice == "2":
                curr_plan_details = self.get_current_plan()
                current_plan = curr_plan_details[0]
                valid_till = curr_plan_details[1]
                if (
                    valid_till > date.today()
                ):  # throws error when cust_id is not registered
                    print()
                    print(current_plan)
                    print("Valid till:", valid_till)
                else:
                    print("\nYour current plan has expired")
            elif choice == "3":
                self.get_recharge_history()
            elif choice == "4":
                self.con.close()
                break
            else:
                print("\nInvalid choice")

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # to display jio plans from file
    def jio_plans(self):
        print("\n")
        with open("jio_plans.txt", "r") as file:
            self.data = file.read()
            self.datalines = file.readlines()
            print(self.data)
        print("\nChoose a recharge plan")
        planNo = input("Choose a recharge plan: ")
        self.jio_recharge(planNo)

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # to display airtel plans from file
    def airtel_plans(self):
        print("\n")
        with open("airtel_plans.txt", "r") as file:
            data = file.read()
            print(data)
        print("\nChoose a recharge plan")
        planNo = input("Choose a recharge plan: ")
        self.airtel_recharge(planNo)

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # to display vi plans from file
    def vi_plans(self):
        print("\n")
        with open("vi_plans.txt", "r") as file:
            data = file.read()
            print(data)
        print("\nChoose a recharge plan")
        planNo = input("Choose a recharge plan: ")
        self.vi_recharge(planNo)

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # to make payment and update database
    def make_payment(self,reciver_accno):
        # Add check payment amount
        # Add payment_method to database
        if self.custbalance >= self.pay:
            # payment_using_accno(self.custaccno) ---> gives error
            self.transaction_obj.pay_amount(reciver_accno,self.pay)
            print(
                f"\nRecharge of Rs. {self.pay} is successful for your number {self.custmobile}."
            )
            self.new_valid_till = date.today() + timedelta(days=self.validity)
            query = "Update customer_recharge set current_plan=%s,valid_till=%s where cust_id=%s"
            val = (self.plan, self.new_valid_till, self.custid)
            self.mycursor.execute(query, val)
            self.con.commit()
            self.insert_recharge_history()
        else:
            print("\nInsufficient balance")

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # initializing attributes using if-else block
    def jio_recharge(self, planNo):
        if planNo == "1":
            self.plan = "Rs. 2999 (Unlimited 5G), Data: 2.5 GB/day, Validity: 365 days"
            self.validity = 365
            self.pay = 2999
            self.make_payment("11111111111")
        elif planNo == "2":
            self.plan = "Rs. 749 (Unlimited 5G), Data: 2 GB/day, Validity: 90 days"
            self.validity = 90
            self.pay = 749
            self.make_payment("11111111111")
        elif planNo == "3":
            self.plan = "Rs. 269 (Unlimited 5G), Data: 1.5 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 269
            self.make_payment("11111111111")
        elif planNo == "4":
            self.plan = "Rs. 666 (Unlimited 5G), Data: 1.5 GB/day, Validity: 84 days"
            self.validity = 84
            self.pay = 666
            self.make_payment("11111111111")
        elif planNo == "5":
            self.plan = "Rs. 199, Data: 1.5 GB/day, Validity: 23 days"
            self.validity = 23
            self.pay = 199
            self.make_payment("11111111111")
        elif planNo == "6":
            self.plan = "Rs. 239 (Unlimited 5G), Data: 1.5 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 239
            self.make_payment("11111111111")
        elif planNo == "7":
            self.plan = "Rs. 179, Data: 1 GB/day, Validity: 24 days"
            self.validity = 24
            self.pay = 179
            self.make_payment("11111111111")
        elif planNo == "8":
            self.plan = "Rs. 149, Data: 1 GB/day, Validity: 20 days"
            self.validity = 20
            self.pay = 149
            self.make_payment("11111111111")
        else:
            print("\nInvalid input")

    def airtel_recharge(self, planNo):
        if planNo == "1":
            self.plan = "Rs. 2999 (Unlimited 5G), Data: 2 GB/day, Validity: 365 days"
            self.validity = 365
            self.pay = 2999
            self.make_payment("22222222222")
        elif planNo == "2":
            self.plan = "Rs. 1499 (Unlimited 5G), Data: 3 GB/day, Validity: 84 days"
            self.validity = 84
            self.pay = 1499
            self.make_payment("22222222222")
        elif planNo == "3":
            self.plan = "Rs. 999 (Unlimited 5G), Data: 2.5 GB/day, Validity: 84 days"
            self.validity = 84
            self.pay = 999
            self.make_payment("22222222222")
        elif planNo == "4":
            self.plan = "Rs. 839 (Unlimited 5G), Data: 2 GB/day, Validity: 84 days"
            self.validity = 84
            self.pay = 839
            self.make_payment("22222222222")
        elif planNo == "5":
            self.plan = "Rs. 779 (Unlimited 5G), Data: 1.5 GB/day, Validity: 90 days"
            self.validity = 90
            self.pay = 779
            self.make_payment("22222222222")
        elif planNo == "6":
            self.plan = "Rs. 699 (Unlimited 5G), Data: 3 GB/day, Validity: 56 days"
            self.validity = 56
            self.pay = 699
            self.make_payment("22222222222")
        elif planNo == "7":
            self.plan = "Rs. 499, Data: 3 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 499
            self.make_payment("22222222222")
        elif planNo == "8":
            self.plan = "Rs. 179, Data: 2 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 179
            self.make_payment("22222222222")
        elif planNo == "9":
            self.plan = "Rs. 155, Data: 1 GB/day, Validity: 24 days"
            self.validity = 24
            self.pay = 155
            self.make_payment("22222222222")
        else:
            print("\nInvalid input")

    def vi_recharge(self, planNo):
        if planNo == "1":
            self.plan = "Rs. 3099 (Unlimited calls + 50 GB extra data), Data: 2 GB/day, Validity: 365 days"
            self.validity = 365
            self.pay = 3099
            self.make_payment("33333333333")
        elif planNo == "2":
            self.plan = "Rs. 359 (Unlimited calls), Data: 3 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 359
            self.make_payment("33333333333")
        elif planNo == "3":
            self.plan = "Rs. 299 (Unlimited calls + 5 GB extra data for 3 days), Data: 1.5 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 299
            self.make_payment("33333333333")
        elif planNo == "4":
            self.plan = "Rs. 195 (Unlimited calls), Data: 3 GB/day, Validity: 30 days"
            self.validity = 30
            self.pay = 195
            self.make_payment("33333333333")
        elif planNo == "5":
            self.plan = "Rs. 179 (Unlimited calls), Data: 2 GB/day, Validity: 28 days"
            self.validity = 28
            self.pay = 179
            self.make_payment("33333333333")
        elif planNo == "6":
            self.plan = "Rs. 459 (Unlimited calls), Data: 6 GB/day, Validity: 84 days"
            self.validity = 84
            self.pay = 459
            self.make_payment("33333333333")
        elif planNo == "7":
            self.plan = "Rs. 204, Data: 500 MB, Validity: 30 days"
            self.validity = 30
            self.pay = 204
            self.make_payment("33333333333")
        elif planNo == "8":
            self.plan = "Rs. 198, Data: 500 MB, Validity: 30 days"
            self.validity = 30
            self.pay = 198
            self.make_payment("33333333333")
        else:
            print("\nInvalid input")

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # returns current recharge plan
    def get_current_plan(self):
        sql = "select current_plan, valid_till from customer_recharge where cust_id=%s"
        val = (self.custid,)
        self.mycursor.execute(sql, val)
        data = self.mycursor.fetchone()
        current_plan = data[0]
        valid_till = data[1]
        return current_plan, valid_till

    def get_recharge_history(self):
        query = "select recharge_history from customer_recharge where cust_id=" + str(
            self.custid
        )
        self.mycursor.execute(query)
        data = self.mycursor.fetchone()[0]
        if data != None:
            filepath = f"Recharge_history_{self.custid}.txt"
            with open(filepath, "wb") as file:
                file.write(data)
            os.startfile(filepath)
        else:
            print("\nNo history found")

    def convertToBinaryData(self, filename):
        file1 = open(filename, "rb")  # to read the content of the file in binary.
        binaryData = file1.read()
        return binaryData

    def insert_recharge_history(self):
        plan = f"PLAN - ₹{self.pay}\n"
        d = datetime.datetime.now()
        ruko = (
            "Purchased on - ",
            d.strftime("%d"),
            d.strftime("%b"),
            d.strftime("%Y"),
            d.strftime("%X"),
        )
        purchased_on = ruko
        payment_mode = f"Payment mode - {self.payment_method}\n"
        ref_no = f"Ref. number - {random.randint(100000000000,999999999999)}\n"
        ruk1 = "Plan start date -", d.strftime("%d"), d.strftime("%b"), d.strftime("%Y")
        start = ruk1
        ruk2 = (
            "Plan end date - ",
            self.new_valid_till.strftime("%d"),
            self.new_valid_till.strftime("%b"),
            self.new_valid_till.strftime("%Y"),
        )
        end = ruk2
        sep = "--------------------------------------\n"
        content = [plan, purchased_on, payment_mode, ref_no, start, end, sep]
        filename = f"Recharge_history_{self.custid}.txt"
        file = open(filename, "a+", encoding="utf-8")
        file.writelines(content)
        file.close()
        query = "Update customer_recharge set recharge_history=%s where cust_id=" + str(
            self.custid
        )
        content = self.convertToBinaryData(filename)
        insert_blob_tuple = (content,)
        self.mycursor.execute(query, insert_blob_tuple)
        self.con.commit()


""" r=Recharge('archanpatel7233@gmail.com')
r.display_menu() """
