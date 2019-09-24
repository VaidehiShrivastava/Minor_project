import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="library")

mycursor = mydb.cursor(prepared=True)
a=input("Scan user rfid:\n")
li = (f"select no_of_books_issued from user where u_rfid='{a}'")
mycursor.execute(li)
records = mycursor.fetchall()

for x in records:
    y=list(x)

print("Number of books issued :",y[0])

if y[0]==0:
    print("You aren't having any books to return")
else:
    b=input("Enter isbn of book you want to return:\n")
    li = (f"select * from issuedbook")
    mycursor.execute(li)
    records = mycursor.fetchall()
    flag=0
    for x in records:
        if x[0]==b and x[1]==a:
            flag=1

    if flag==1:
        mycursor = mydb.cursor(prepared=True)
        sel_user=(f"select no_of_books_issued from user where u_rfid='{a}'")
        sel_book=(f"select no_of_copies from book where isbn='{b}'")

        mycursor.execute(sel_user)
        ibook=mycursor.fetchall()
        books=list(ibook[0])
        if books[0]>0:

            try:
                mycursor.execute(f"delete from issuedbook where ub_rfid='{a}' and b_rfid='{b}'")
                mydb.commit()
                print("deleted 1 row from issuedbook")
            except:
                print("SQL exception : tuple not found")

            mycursor.execute (f"update user set no_of_books_issued={books[0]-1} where u_rfid='{a}'")
            mydb.commit()
            print("removed 1 book from number of books issued from user table")

            mycursor.execute(sel_book)
            ubook = mycursor.fetchall()
            copies = list(ubook[0])
            if copies[0]<5:
                mycursor.execute(f"update book set no_of_copies={copies[0] + 1} where isbn='{b}'")
                mydb.commit()
                print("added 1 book into number of copies in book table")
            else:
                print("copies exceeeded max limit")

        else:
            print("cant delete; limit reached zero")
        # mycursor.execute (f"update user set no_of_books_issued={y[0]-1} where userid={a}")
    else:
        print("book isnt in your record")


