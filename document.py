from tkinter import filedialog
import tkinter as tk
import mysql.connector
import backend
import os
class document:
    def __init__(self,email):
        # constructor for connection
        self.con = mysql.connector.connect(
            host="localhost", user="root", password="", database="group_project_python"
        )
        self.mycursor = self.con.cursor()
        backend_obj=backend.Customer()
        backend_obj.getall(email)
        self.cust_id=backend_obj.custid

    def getdocumentcontent(self, docid):
        query = "select doc_content from customer_document where doc_id=%s"
        val = (docid,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchone()
        for i in rs:
            row_str = i
        return row_str

    def choose_file(self, root):
        file_path = filedialog.askopenfilename()
        root.destroy()
        if file_path == "" or file_path == None:
            print("Please Select The Document!")
            self.selectdocument()
        else:
            print("Selected Document:", file_path)
            istitle = False
            while istitle != True:
                title = input("Enter The Document Title : ")
                if self.checkexsistdocument(title) == False:
                    istitle = True
                else:
                    print("this document is already exsits")
                    self.selectdocument()
                    istitle = True
            file1 = open(file_path, "rb")
            content = file1.read()
            query = "insert into customer_document(cust_id,doc_title,doc_path,doc_extension,doc_content) values(%s,%s,%s,%s,%s)"
            start = file_path.rfind(".")
            extension = file_path[start:]
            val = (self.cust_id, title, file_path, extension, content)
            self.mycursor.execute(query, val)
            self.con.commit()

    def checkiddocument(self, id):
        isid = False
        query = "select doc_id from customer_document where cust_id=%s"
        val = (self.cust_id,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            row_str = ",".join(str(element) for element in i)
            if int(row_str) == id:
                isid = True
                break
            else:
                isid = False
        return isid

    def getdoctitle(self, docid):
        query = "select doc_title,doc_extension from customer_document where doc_id=%s"
        val = (docid,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchone()
        return

    def selectdocument(self):
        root = tk.Tk()
        root.title("File Chooser Example")
        button = tk.Button(
            root, text="Choose File", command=lambda: self.choose_file(root)
        )
        button.pack(pady=20)
        root.mainloop()

    def getdocument(self):
        query = "select doc_id,doc_title from customer_document where cust_id=%s"
        val = (self.cust_id,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            print("Enter ", i[0], " For Download ", i[1])
        choice = int(input("Enter Your Choice : "))
        if self.checkiddocument(choice):
            row_str = self.getdocumentcontent(choice)
            query = (
                "select doc_title,doc_extension from customer_document where doc_id=%s"
            )
            val = (choice,)
            self.mycursor.execute(query, val)
            rs = self.mycursor.fetchone()
            file_name=rs[0]+rs[1]
            f = open(file_name, "wb")
            f.write(row_str)
            f.close()
            os.startfile(file_name)
        else:
            print("Please Enter Valid Choice!")

    def checkexsistdocument(self, title):
        isdocument = False
        query = "select doc_title from customer_document where cust_id=%s"
        val = (self.cust_id,)
        self.mycursor.execute(query, val)
        rs = self.mycursor.fetchall()
        for i in rs:
            row_str = ",".join(str(element) for element in i)
            if row_str == title:
                isdocument = True
                break
            else:
                isdocument = False
        return isdocument
