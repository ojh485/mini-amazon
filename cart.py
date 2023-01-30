from flask import current_app as app


class Cart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, id, uid, pid, sid, seller, quantity, name, price):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.seller = seller
        self.quantity = quantity
        self.name = name
        self.price = price


    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT Carts.id as id, Carts.uid as uid, Carts.pid as pid, Carts.sid as sid, CONCAT(Users.firstname, \' \', Users.lastname) as seller, quantity, name, price
FROM Carts, Products, Users
WHERE Carts.pid = Products.id
AND Carts.uid = :uid
AND Users.id = Carts.sid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_total(uid):
        n = app.db.execute('''
SELECT SUM(quantity*price)
FROM Carts, Products
WHERE Carts.pid = Products.id
AND uid = :uid
''',
                              uid=uid)
        if n[0][0] == None:
            return 0
        return n[0][0]

    @staticmethod
    def changeQuantity(prodname, newquant, uid):
        
        try:
            pid = app.db.execute('''
SELECT id
FROM Products
WHERE name = :prodname
''',
                              prodname=prodname)
            pid = pid[0][0]
            print(pid)
        
        except Exception as e:
            print(str(e))
            return None
        
        try:
            rows = app.db.execute("""
UPDATE Carts
SET quantity=:newquant
WHERE pid = :pid
AND uid = :uid
""",
                                  newquant=newquant, pid=pid, uid=uid)
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    def deleteItem(prodname, uid):
        
        try:
            pid = app.db.execute('''
SELECT id
FROM Products
WHERE name = :prodname
''',
                              prodname=prodname)
            pid = pid[0][0]
            print(pid)
        
        except Exception as e:
            print(str(e))
            return None
        
        try:
            rows = app.db.execute("""
DELETE FROM carts
WHERE pid = :pid
AND uid = :uid
""",
                                  pid=pid, uid=uid)
        except Exception as e:
            print(str(e))
            return None

    
    @staticmethod
    def placeOrder(uid):

        
        
        # ensure sellers have enough quantity
        try:
            overs = app.db.execute("""
SELECT COUNT(*)
FROM Carts, Sells
WHERE Carts.uid = :uid
AND Carts.sid = Sells.uid
AND Carts.pid = Sells.pid
AND Carts.quantity > Sells.quantity
""",
                                  uid=uid)[0][0]
        except Exception as e:
            print(str(e))
        
        if overs > 0:
            return None
        
        # ensure balance > cart price
        price = Cart.get_total(uid)

        balance = app.db.execute("""
SELECT balance
FROM Users
WHERE Users.id = :uid
""",
                                uid=uid)[0][0]
        
        if price > balance:
            print('over')
            return None

        # update balance
        app.db.execute("""
UPDATE Users
SET balance = balance - :price
WHERE id = :uid
""",
                                  uid=uid, price=price)


        
        cart_rows = Cart.get_by_uid(uid)
        for item in cart_rows:
            pid = item.pid
            sid = item.sid    
            quantity = item.quantity
            p = item.price

            # add items to purchases
            app.db.execute("""
INSERT INTO Purchases(uid, pid, sid, quantity)
VALUES(:uid, :pid, :sid, :quantity)
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity)

            # truncate generated timestamps on seconds                        
            app.db.execute("""
UPDATE Purchases
SET time_purchased = DATE_TRUNC('second', time_purchased)
WHERE pid = :pid
AND uid = :uid
AND sid = :sid
AND quantity = :quantity
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity)

            # update seller balance
            app.db.execute("""
UPDATE Users
SET balance = balance + (:price * :quantity)
WHERE id = :sid
""",
                                  sid=sid, price=p, quantity=quantity)

            # update seller quantity
            app.db.execute("""
UPDATE Sells
SET quantity = quantity - :quantity
WHERE uid = :sid
AND pid = :pid
""",
                                  sid=sid, pid=pid, quantity=quantity)

            # remove items from cart
            app.db.execute("""
DELETE FROM Carts
WHERE uid = :uid
AND pid = :pid
AND sid = :sid
AND quantity = :quantity
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity)
        

        return None

    @staticmethod
    def add_to_cart(uid, pid, sid, quant):

        numAvailable = app.db.execute('''
SELECT quantity
FROM Sells
WHERE uid = :sid AND pid = :pid
''',
                              sid=sid, 
                              pid=pid,
                              )
        if numAvailable[0][0] - quant > 0:

            numInCart = app.db.execute('''
    SELECT COUNT(id) as count
    FROM Carts
    WHERE uid = :uid AND pid = :pid AND sid = :sid
    ''',
                                uid=uid, 
                                pid=pid,
                                sid=sid,
                                quant = quant)

            if numInCart[0][0] > 0:
                updateItem = app.db.execute("""
        UPDATE Carts
        SET quantity= quantity + :quant
        WHERE pid = :pid
        AND uid = :uid
        """,
                                    pid=pid, uid=uid, quant = quant)
                return None
            else:
                insertItem = app.db.execute('''
        INSERT INTO Carts(uid, pid, sid, quantity)
        VALUES(:uid, :pid, :sid, :quant)
        ''',
                                    uid=uid, 
                                    pid=pid,
                                    sid=sid,
                                    quant = quant
                                    )
                return None


class Order:
    def __init__(self, id, uid, pid, sid, seller, quantity, name, price, time, item_status, order_status):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.seller = seller
        self.quantity = quantity
        self.name = name
        self.price = price
        self.time = time
        self.item_status = item_status
        self.order_status = order_status


    @staticmethod
    def get_orders_by_uid(uid):
        rows = app.db.execute('''
SELECT Purchases.uid as uid, SUM(quantity) as quantity, SUM(quantity*price) as price, time_purchased as time, order_status, Purchases.pid as pid, Purchases.sid as sid, CONCAT(Users.firstname, \' \', Users.lastname) as seller, Products.name as name
FROM Purchases, Users, Products
WHERE Purchases.uid = :uid
AND Users.id = Purchases.sid
AND Purchases.pid = Products.id
GROUP BY time_purchased, order_status, purchases.uid, name, seller, sid, pid
ORDER BY time_purchased DESC
''',
                                uid=uid)
        return rows

    @staticmethod
    def get_order(uid, time_purchased):
        rows = app.db.execute('''
SELECT Purchases.id as id, Purchases.uid as uid, Purchases.pid as pid, Purchases.sid as sid, CONCAT(Users.firstname, \' \', Users.lastname) as seller, 
quantity, Products.name as name, price, time_purchased as time, item_status, order_status
FROM Purchases, Users, Products
WHERE Purchases.uid = :uid
AND time_purchased = :time_purchased
AND Users.id = Purchases.sid
AND Purchases.pid = Products.id
ORDER BY time_purchased DESC, Products.name
''',
                                uid=uid, time_purchased=time_purchased)
        return [Order(*row) for row in rows]