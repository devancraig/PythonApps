import mysql.connector
from mysql.connector import Error

def delete_sqlinfo(sql):
    connection = mysql.connector.connect(
    host="us-cdbr-iron-east-04.cleardb.net",
    user="b0937237df5488",
    passwd="fd54464a",
    database="heroku_bcead2b1728a15f"
    )

    # sql_select_Query = "select * from Person1"
    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()


sql = "DELETE FROM person1 WHERE Id = 122"
delete_sqlinfo(sql)
# sell = [0,0,0,0,1]
# i = 0
# for row in records:
#     if(sell[i] == 1):
#         print("balance = ", row[1], )
#         print("stockname = ", row[2])
#         print("price  = ", row[3])
#         print("amount  = ", row[4], "\n")
#     i = i + 1


