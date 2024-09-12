import random
from backend import Customer as cust
import Transaction as tran
customer = cust()


class Paybills:
    def __init__(self,user_email):
        self.transaction_obj = tran.Transaction(user_email)
    def paybills(self,reciver_accno):
        mobilenumber = customer.checkdigit("Enter Registered Mobile Number : ")
        if customer.existsmobilenumber(mobilenumber):
            city = customer.checkalpha("Enter Your City : ")
            address = customer.checkalphadigcomp("Enter Your Address : ")
            amount=random.randint(1000, 3000)
            print("Your Bill Is : ", amount)
            self.transaction_obj.pay_amount(reciver_accno,amount)
        else:
            print("Please Enter Registered Number!")
            return self.paybills()

    def paybills_option(self):
        while True:
            print("Enter 1 For Pay Electricity Bill")
            print("Enter 2 For Pay Gas Bill")
            print("Enter 3 For Back")
            print("Enter 4 For Exit")
            ch = input("Enter Your Choice : ")
            match ch:
                case "1":
                    while True:
                        print("Enter 1 For Torrent Power")
                        print("Enter 2 For Adani Power")
                        print("Enter 3 For Back")
                        print("Enter 4 For Exit")
                        ch1 = input("Enter Your Choice : ")
                        match ch1:
                            case "1":
                                self.paybills("44444444444")
                                break
                            case "2":
                                self.paybills("55555555555")
                                break
                            case "3":
                                return
                            case "4":
                                exit()
                            case _:
                                print("Please Enter Valid Choice!")
                case "2":
                    while True:
                        print("Enter 1 For Adani Gas Company")
                        print("Enter 2 For Indian Oil Gas Company")
                        print("Enter 3 For Hp Gas Company")
                        print("Enter 4 For Back")
                        print("Enter 5 For Exit")
                        ch1 = input("Enter Your Choice : ")
                        match ch1:
                            case "1":
                                self.paybills("66666666666")
                                break
                            case "2":
                                self.paybills("77777777777")
                                break
                            case "3":
                                self.paybills("88888888888")
                                break
                            case "4":
                                return
                            case "5":
                                exit()
                            case _:
                                print("Please Enter Valid Choice!")
                    pass
                case "3":
                    return
                case "4":
                    exit()
                case _:
                    print("Please Enter Valid Choice!")
