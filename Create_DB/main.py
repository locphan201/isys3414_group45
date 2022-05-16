import mysql.connector

def connect_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )
    cursor = mydb.cursor()
    return mydb, cursor

def disconnect_db(mydb, cursor):
    cursor.close()
    mydb.close()
    return mydb, cursor

def s(mydb, cursor):
    with open('db.txt', 'r', encoding='UTF-8') as f:
        query = f.readline()
        
        while query != '':
            cursor.execute(query)
            query = f.readline()
        mydb.commit()
    
def main(mydb, cursor):
    s(mydb, cursor)
    
if __name__ == '__main__':
    mydb, cursor = connect_db()
    main(mydb, cursor)
    mydb, cursor = disconnect_db(mydb, cursor)