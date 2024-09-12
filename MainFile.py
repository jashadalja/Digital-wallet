import Transaction as tran
import backend as back
import paymentreminder as pr
import requestpayment as rp
import document as dc
import recharge as recharge
import paybills as pb
import rewards as rd
class Digital_Wallet:
    def __init__(self) -> None:
        self.backend_obj = back.Customer()

    def choose_auth_option(self):
        print("------------------------------------------------------------")
        print("Enter 1 For Sign-up")
        print("Enter 2 For Login")
        print("Enter 3 For Exit!")
        choice = None
        while not choice:
            choice = input("Enter Your Choice : ")
        choice = int(choice)
        match choice:
            case 1:
                self.backend_obj.customer_signup()
                self.email_id = self.backend_obj.cust_email
                self.main_option()
            case 2:
                self.backend_obj.cust_login()
                self.email_id = self.backend_obj.cust_email
                self.main_option()
            case 3:
                print("Thank You !!")
                exit(0)
            case _:
                print("Please Enter Valid Choice !!")
        self.choose_auth_option()

    def main_option(self):
        print("------------------------------------------------------------")
        print("Enter 1 For Payment Section : ")
        print("Enter 2 For Document Section : ")
        print("Enter 3 for logout : ")
        print("Enter 4 for Exit")
        choice = None
        while not choice:
            choice = input("Enter Your Choice : ")
        choice = int(choice)
        match choice:
            case 1:
                self.tran_option()
            case 2:
                self.document_option()
            case 3:
                self.choose_auth_option()
            case 4:
                print("Thank You !!")
                exit(0)
            case _:
                print("Please Enter Valid Choice!")
        self.main_option()

    def tran_option(self):
        print("------------------------------------------------------------")
        print("Enter 1 For Transaction Options")
        print("Enter 2 For Transaction History")
        print("Enter 3 For Payment Reminder")
        print("Enter 4 For Recharge")
        print("Enter 5 For Pay Bills")
        print("Enter 6 For Rewards")
        print("Enter 7 For Help")
        print("Enter 8 For Request Payment")
        print("Enter 9 For Request Payment options")
        print("Enter 10 For back")
        print("Enter 11 For Exit")
        choice = None
        while not choice:
            choice = input("Enter Your Choice : ")
        choice = int(choice)
        self.transaction_obj = tran.Transaction(self.email_id)
        self.paymentReminder_obj = pr.paymentr(self.email_id)
        self.paymentRequest_obj = rp.request(self.email_id)
        self.recharge_obj=recharge.Recharge(self.email_id)
        paybills_obj=pb.Paybills(self.email_id)
        match choice:
            case 1:
                self.transaction_obj.make_payment()
            case 2:
                self.transaction_obj.print_history()
            case 3:
                self.paymentReminder_obj.payment_reminder()
            case 4:
                self.recharge_obj.display_menu()
            case 5:
                paybills_obj.paybills_option()
            case 6:
                rd.getrewards(2)
            case 7:
                import webbrowser
                url = "https://www.jiocinema.com/"
                webbrowser.get().open(url)
            case 8:
                self.paymentRequest_obj.request_payment()
            case 9:
                self.paymentRequest_obj.request_paymentoptions()
            case 10:
                self.main_option()
            case 11:
                print("Thank You !!")
                exit(0)
            case _:
                print("Please Enter Valid Choice!")
        self.tran_option()

    def document_option(self):
        print("------------------------------------------------------------")
        print("Enter 1 For Upload Documents")
        print("Enter 2 For Get Documents")
        print("Enter 3 For Back")
        print("Enter 4 For Exit")
        choice = None
        while not choice:
            choice = input("Enter Your Choice : ")
        choice = int(choice)
        self.document_obj = dc.document(self.email_id)
        match choice:
            case 1:
                self.document_obj.selectdocument()
            case 2:
                self.document_obj.getdocument()
            case 3:
                self.main_option()
            case 4:
                print("Thank You !!")
                exit(0)
            case _:
                print("Please Enter Valid Choice!")
        self.document_option()


dw = Digital_Wallet()
dw.choose_auth_option()
