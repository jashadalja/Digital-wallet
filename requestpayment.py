import mysql.connector
import backend
import Transaction as tran

class request:
    def __init__(self, email):
        # constructor for connection
        self.con = mysql.connector.connect(
            host="localhost", user="root", password="", database="group_project_python" ,autocommit=True
        )
        self.mycursor = self.con.cursor()
        self.backend_obj = backend.Customer()
        self.backend_obj.getall(email)
        self.custmobile = self.backend_obj.custmobile
        self.custaccno = self.backend_obj.custaccno
        self.transaction_obj = tran.Transaction(email)

    def alreadyrequest(self, mobileno):
        isalready = False
        sql = "select person_mobileno from customer_requestpayment where cust_mobileno=%s and person_mobileno=%s"
        val = (self.custmobile, mobileno)
        self.mycursor.execute(sql, val)
        r = self.mycursor.fetchall()
        for i in r:
            if i != "":
                isalready = True
        return isalready

    def updateamount(self, mobileno, amount):
        sql = "update customer_requestpayment set amount=amount+%s where cust_mobileno=%s and person_mobileno=%s"
        val = (amount, self.custmobile, mobileno)
        self.mycursor.execute(sql, val)
        self.con.commit()

    def checkidrequest(self, id):
        id = int(id)
        isid = False
        query = "select rpid from customer_requestpayment where person_mobileno=%s"
        val = (self.custmobile,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            if int(i[0]) == id:
                isid = True
                break
            else:
                isid = False
        return isid

    def request_payment(self):
        ismobile = False
        while ismobile != True:
            mobileno = input(
                "Enter The Mobile Number Of Person From Whom You Want Payment :"
            )
            if mobileno != self.custmobile:
                if self.backend_obj.existsmobilenumber(mobileno):
                    if self.alreadyrequest(mobileno):
                        isamount = False
                        while isamount != True:
                            amount = input("Enter The Amount : ")
                            if amount.isdigit():
                                isamount = True
                            else:
                                print("Please Enter Valid Amount!")
                                isamount = False
                        self.updateamount(mobileno, amount)
                        ismobile = True
                    else:
                        isamount = False
                        while isamount != True:
                            amount = input("Enter The Amount : ")
                            if amount.isdigit():
                                isamount = True
                            else:
                                print("Please Enter Valid Amount!")
                                isamount = False
                        sql = "insert into customer_requestpayment(cust_mobileno,person_mobileno,amount)values(%s,%s,%s)"
                        val = (self.custmobile, mobileno, amount)
                        self.mycursor.execute(sql, val)
                        self.con.commit()
                        ismobile = True
                else:
                    ismobile = False
                    print("Enter Valid Number!")
            else:
                ismobile = False
                print("Ohh This is Your Number!")

    def request_paymentoptions(self):
        query = "select rpid,cust_mobileno,amount from customer_requestpayment where person_mobileno=%s"
        val = (self.custmobile,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        isoption = False
        for i in rs:
            reciver_mobile=i[1]
            amount=i[2]
            if i != "":
                isoption = True
            """  row_str = ",".join(str(element) for element in i)
            z = row_str.split(",") """
            print(
                i[1],
                " has requested amount : ",
                i[2],
                " enter ",
                i[0],
                " for do the payment!",
            )
        if isoption:
            ischoice = False
            while ischoice != True:
                choice = input("Enter Your Choice : ")
                if choice.isdigit():
                    ischoice = True
                else:
                    print("Please Enter Valid Choice!")
                    ischoice = False
            if self.checkidrequest(choice) == True:
                reciver_accno=self.fatch_accnno(reciver_mobile)
                self.transaction_obj.set_updates(self.custaccno,reciver_accno,amount)
                sql = "delete from customer_requestpayment WHERE person_mobileno = %s "
                val = (self.custmobile,)
                self.mycursor.execute(sql, val)
                
                # call the transaction methods
            else:
                print("Please Enter Valid Choice!")
        else:
            print("not requested yet")

    def fatch_accnno(self, phone_no):
        sql = """SELECT t1.cust_accno
                 FROM customer_bankinfo t1
                 INNER JOIN customer_info t2 ON t1.cust_id = t2.cust_id
                 WHERE t2.cust_mobileno = %s """
        val = (phone_no,)
        self.mycursor.execute(sql, val)
        accno = self.mycursor.fetchone()[0]
        return accno
