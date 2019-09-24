import mysql.connector
from datetime import datetime
from datetime import timedelta

mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="library")

mycursor = mydb.cursor(prepared=True)

a=input("Scan user rfid:\n")
case1=(f"select u_rfid from user where u_rfid='{a}'")
mycursor.execute(case1)
users=mycursor.fetchall()
u1=False
for i in users:
     if i[0]==a:
        u1=True
        break

if u1==True:

        li = (f"select no_of_books_issued from user where u_rfid='{a}'")
        mycursor.execute(li)
        records1 = mycursor.fetchall()

        for x in records1:
            y=list(x)

        print("Number of books issued :",y[0])

        if y[0]==5:
            print("Exceeded max limit: cant issue more than 5 books")
        else:
                b=input("Enter isbn of book you want to issue:\n")
                li = (f"select * from issuedbook")
                mycursor.execute(li)
                records = mycursor.fetchall()

                case2=(f"select isbn from book where isbn='{b}'")
                mycursor.execute(case2)
                books=mycursor.fetchall()
                b1=False
                for j in books:
                    if j[0] == b:
                        b1 =True
                        break



                if u1==True and b1==False:
                    print("wrong isbn for book")
                else:
                    flag = 0
                    for x in records:
                        if x[0] == b and x[1] == a:
                            flag = 1
                    if flag == 1:
                        print("already issued")
                    else:
                        mycursor = mydb.cursor(prepared=True)
                        sel_user = (f"insert into issuedbook(b_rfid,ub_rfid) values('{b}','{a}')")
                        mycursor.execute(sel_user)
                        mydb.commit()

                        print("book inserted in issued book")

                        sel_book = (f"select no_of_copies from book where isbn='{b}'")

                        mycursor.execute(sel_book)
                        ibook = mycursor.fetchall()
                        books = list(ibook[0])
                        if books[0] > 0:

                            mycursor.execute(f"update book set no_of_copies={books[0] - 1} where isbn='{b}'")
                            mydb.commit()
                            print("removed 1 book from number of copies available for issue")

                            sel_user = (f"select no_of_books_issued from user where u_rfid='{a}'")
                            mycursor.execute(sel_user)
                            ubook = mycursor.fetchall()
                            copies = list(ubook[0])
                            if copies[0] < 5:
                                mycursor.execute(f"update user set no_of_books_issued={copies[0] + 1} where u_rfid='{a}'")
                                mydb.commit()
                                print("added 1 book into number of books issued to user")
                                i=datetime.now().date()
                                mycursor.execute(f"update issuedbook set issue_date='{i}' where b_rfid='{b}' and ub_rfid='{a}'")
                                mydb.commit()
                                print("issue date updated")
                                j=datetime.now().date()+timedelta(days=15)
                                mycursor.execute(f"update issuedbook set return_date='{j}' where b_rfid='{b}' and ub_rfid='{a}'")
                                mydb.commit()
                                print("return date updated")

                            else:print("cant issue")


                        else:
                            print("cant issue; book isnt avaialable")

else:
    print(" hey you are not our user :{ hurr hurr!!")

