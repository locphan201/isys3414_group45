import mysql.connector

# Connecting to the database
def connect_db():
    mydb = mysql.connector.connect(
        host="eu-cdbr-west-02.cleardb.net",
        user="b03249ea8f4171",
        password="4bf170a0"
    )
    cursor = mydb.cursor()
    db = "USE heroku_6424eae9f05fcc3"
    cursor.execute(db)
    return mydb, cursor

    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="123456"
    # )
    # cursor = mydb.cursor()
    # db = "USE nanasbakery"
    # cursor.execute(db)
    # return mydb, cursor

def disconnect_db():
    global mydb, cursor
    cursor.close()
    mydb.close()
    
mydb, cursor = connect_db()

# Login
def check_login(account, password):
    global mydb, cursor
    query = """SELECT spwd 
               FROM Staffs
               WHERE sphone='%s'
            """ %account
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    else:
        return result[0][0] == password
    
# Customers
def get_customer(cID):
    global mydb, cursor
    query = """SELECT * 
               FROM Customers
               WHERE cID=%s
            """ %cID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return
    return result[0]

def update_customer(cID, name, phone, addr, email, pwd):
    global mydb, cursor
    query = """UPDATE Customers
               SET cname='%s', cphone='%s', caddress='%s', cemail='%s', cpwd='%s'
               WHERE cID=%s
            """ %(name, phone, addr, email, pwd, cID)
    cursor.execute(query)
    mydb.commit()
    
def delete_customer(cID):
    global mydb, cursor
    query = """SELECT cID
               FROM Customers
               WHERE cID=%s
            """ %cID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    query = """DELETE FROM Customers
               WHERE cID=%s
            """ %cID
    cursor.execute(query)
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    mydb.commit()

def get_total_customers():
    global mydb, cursor
    query = """ SELECT COUNT(cID)
                FROM Customers
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    return result[0][0]

# Orders
def get_order_info(oID):
    global mydb, cursor
    query = """SELECT pname, quantity, price
               FROM products P, contains C
               WHERE P.pID = C.pID AND C.oID = %s
            """ %oID
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def get_incompleted_orders():
    global mydb, cursor
    query = """SELECT O.oID, C.cname, C.cphone, O.price
               FROM Orders O, Customers C
               WHERE O.cID = C.cID AND type='INCOMPLETED'
               ORDER BY oID ASC LIMIT 15
            """
    cursor.execute(query)
    result = cursor.fetchall()
    
    order_items = []
    for i in result:
        order_items.append(get_order_info(i[0]))
    return result, order_items

def update_order_status(oID, status):
    global mydb, cursor
    query = """UPDATE Orders
               SET type='%s'
               WHERE oID=%s
               """ %(status, oID)
    cursor.execute(query)
    mydb.commit()
        
def get_total_income():
    global mydb, cursor
    query = """SELECT SUM(price)
               FROM Orders
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0 
    return result[0][0]
    
def get_all_orders():
    order = []
    global mydb, cursor
    query = """SELECT COUNT(oID)
               FROM Orders
               WHERE type = 'COMPLETED'
               GROUP BY type
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        order.append(0)
    else:
        order.append(result[0][0])
        
    query = """SELECT COUNT(oID)
               FROM Orders
               WHERE type = 'INCOMPLETED'
               GROUP BY type
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        order.append(0)
    else:
        order.append(result[0][0])
        
    query = """SELECT COUNT(oID)
               FROM Orders
               WHERE type = 'CANCELLED'
               GROUP BY type
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        order.append(0)
    else:
        order.append(result[0][0])
    return order

def get_avg():
    global mydb, cursor
    query = """SELECT FORMAT(AVG(price),2)
               FROM Orders
               WHERE type != 'CANCELLED'
            """
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    return result[0][0]

# Products
def update_product(pID, name, price):
    global mydb, cursor
    query = """UPDATE Products
               SET pname='%s', price=%s
               WHERE pID=%s
            """ %(name, price, pID)
    cursor.execute(query)
    mydb.commit()
      
def delete_product(pID):
    global mydb, cursor
    query = """SELECT pID
               FROM Products
               WHERE pID=%s
            """ %pID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        
        return
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    query = """DELETE FROM Products
               WHERE pID=%s
            """ %pID
    cursor.execute(query)
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    mydb.commit()
     
def get_product(pID):
    global mydb, cursor
    query = """SELECT *
               FROM Products
               WHERE pID=%s
            """ %pID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        
        return
    
    return result[0]

def get_best_sellers():
    global mydb, cursor
    query = """SELECT P.pname, SUM(C.quantity)
               FROM products P, contains C 
               WHERE P.pID = C.pID 
               GROUP BY C.pID 
               ORDER BY SUM(C.quantity) DESC LIMIT 5"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Employees
def update_employee(eID, name, phone, salary, email, pos, pwd):
    global mydb, cursor
    query = """UPDATE Staffs
               SET sname='%s', sphone='%s', salary=%s, semail='%s', sposition='%s', spwd='%s'
               WHERE sID=%s
            """ %(name, phone, salary, email, pos, pwd, eID)
    cursor.execute(query)
    mydb.commit()
        
def delete_employee(eID):
    global mydb, cursor
    query = """SELECT sID
               FROM Staffs
               WHERE sID=%s
            """ %eID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        
        return
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    query = """DELETE FROM Staffs
               WHERE sID=%s
            """ %eID
    cursor.execute(query)
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    mydb.commit()
     
def get_employee(eID):
    global mydb, cursor
    query = """SELECT *
               FROM Staffs
               WHERE sID=%s
            """ %eID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0: 
        return
    return result[0]

def add_employee(name, phone, salary, email, pos, pwd):
    global mydb, cursor
    query = """INSERT INTO Staffs (sname, sphone, salary, semail, sposition, spwd)
               VALUES ('%s', '%s', %s, '%s', '%s', '%s')
            """ %(name, phone, salary, email, pos, pwd)
    cursor.execute(query)
    mydb.commit()
    
# Accounting
def update_accounting(aID, date, description, type, amount):
    global mydb, cursor
    query = """UPDATE Accounting
               SET date='%s', description='%s', type='%s', amount=%s
               WHERE aID=%s
            """ %(date, description, type, amount, aID)
    cursor.execute(query)
    mydb.commit()
      
def delete_accounting(aID):
    global mydb, cursor
    query = """SELECT aID
               FROM Accounting
               WHERE aID=%s
            """ %aID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        
        return
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    query = """DELETE FROM Accounting
               WHERE aID=%s
            """ %aID
    cursor.execute(query)
    query = """SET FOREIGN_KEY_CHECKS = 0""" 
    cursor.execute(query)
    mydb.commit()
      
def get_accounting(aID):
    global mydb, cursor
    query = """SELECT *
               FROM Accounting
               WHERE aID=%s
            """ %aID
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return
    return result[0]

def add_accounting(date, description, type, amount):
    global mydb, cursor
    query = """INSERT INTO Accounting (date, description, type, amount)
               VALUES ('%s', '%s', '%s', %s)
            """ %(date, description, type, amount)
    cursor.execute(query)
    mydb.commit()
   
# Others
def get_monthly_numOrders():
    numOrders = []
    global mydb, cursor
    for month in range(1,13):
        query = """SELECT COUNT(oID)
                   FROM Orders
                   WHERE type != 'CANCELLED' AND MONTH(date) = %s
                   GROUP BY MONTH(date)
                """ %month
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            numOrders.append(0)
        else:
            numOrders.append(result[0][0])
    
    return numOrders

def get_monthly_revenue():
    revenue, expense = [], []
    global mydb, cursor
    for month in range(1,13):
        query = """SELECT SUM(price)
                   FROM Orders
                   WHERE type != 'CANCELLED' AND MONTH(date) = %s
                   GROUP BY MONTH(date);
                """ %month
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            revenue.append(0)
        else:
            revenue.append(result[0][0])
        query = """SELECT SUM(amount)
                   FROM Accounting
                   WHERE type = 'Spend' AND MONTH(date) = %s
                   GROUP BY MONTH(date)
                """ %month
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            expense.append(0)
        else:
            expense.append(result[0][0])
    
    return [revenue, expense]