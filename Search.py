import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="library")

# mycursor = mydb.cursor(prepared=True)
#a='101cs'
# li = (f"select no_of_copies from book where isbn={a}")
# mycursor.execute(li)
# records = mycursor.fetchall()
#
# for x in records:
#     y=list(x)
#
# print(y)


mycursor=mydb.cursor(prepared=True)
name='datastructure'
mycursor.execute (f"select isbn from book where title='{name}'")
records = mycursor.fetchall()

for x in records:
    print(x[0])


#mydb.commit()

mycursor.execute (f"select * from book where isbn='{x[0]}'")
records = mycursor.fetchall()

for x in records:
    print(x)






