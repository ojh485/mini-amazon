from flask import current_app as app

class Inventory:
    def __init__(self, id, uid, pid, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity


    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity
FROM Sells
WHERE pid = :pid
''',
                              pid=pid)
        return Inventory(*(rows[0])) if rows else None


    @staticmethod
    def get_by_id(id):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity
FROM Sells
WHERE id = :id
''',
                              id=id)
        return Inventory(*(rows[0])) if rows else None


    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity
FROM Sells
WHERE uid = :uid
''',
                              uid=uid)
        return [Inventory(*row) for row in rows]if rows else None


    @staticmethod
    def get_seller_inventory(uid):
        rows = app.db.execute('''
SELECT Sells.pid, name, price, category, description, image, quantity, Sells.id
FROM Sells, Products
WHERE uid = :uid
AND Sells.pid = Products.id
''',
                            uid = uid)
        return rows

    
    @staticmethod
    def get_item_by_id(uid, id):
        rows = app.db.execute('''
SELECT Sells.pid, name, price, category, description, image, quantity, Sells.id
FROM Sells, Products
WHERE uid = :uid
AND Sells.pid = Products.id
''',
                            uid = uid)
        item = ""
        for i in rows:
            if i.id == id:
                item = i
        return item

    
    @staticmethod
    def add_item(uid, name, price, category, description, quantity, image):
        available = "False"
        if quantity > 0:
            available = "True"
        product_page = 'product_page'
        check = app.db.execute("""
SELECT *
FROM Products
WHERE name = :name
""",
                name=name)
        #check to see if the product already exists
        if not check:
            insert1 = app.db.execute("""
INSERT INTO Products(name, price, available, category, description, product_page, image)
VALUES(:name, :price, :available, :category, :description, :product_page, :image)
RETURNING id
""",
                name=name, price=price, available=available, category=category,
                description=description, product_page=product_page,
                image=image)
            pid = insert1[0][0]
            new_review = app.db.execute("""
INSERT INTO Reviews(uid, pid, stars, review)
VALUES(:uid, :pid, :stars, :review)
RETURNING id
""",
                            
                                  uid = uid,
                                  pid = pid, stars = 5, review = "Marketplace loves your product!")
        else:
            available = "True"
            update = app.db.execute("""
UPDATE Products
SET available = :available
WHERE name = :name
""",
                name=name, available = available)
            pid = check[0][0]
        insert2 = app.db.execute("""
INSERT INTO Sells(uid, pid, quantity)
VALUES(:uid, :pid, :quantity)
RETURNING id
        """,
                uid=uid, pid=pid, quantity=quantity)
        sid = insert2[0][0]
        return sid


    # edit quantity
    @staticmethod
    def changequantity(id, quantity):
        row = app.db.execute("""
UPDATE Sells
SET quantity = :quantity
WHERE id = :id
""",
                id=id, quantity=quantity)
        return row
    
    # delete item from Sells and change product to Unavailable
    @staticmethod
    def deleteinventory(id):
        item = app.db.execute("""
SELECT *
FROM Sells
WHERE id = :id
""",
                id = id)
        pid = item[0][2]
        leftover = app.db.execute("""
SELECT *
FROM Products
WHERE id = :pid
""",
                pid=pid)
        if not leftover:
            update = app.db.execute("""
UPDATE Products
SET availabe = "False"
WHERE pid = :pid
""",
                    pid=pid)
        deleteinsells = app.db.execute("""
DELETE FROM Sells
WHERE id = :id
""",
                id = id)
        return deleteinsells

    
    # pull info from Purchases to fill orders for specific seller
    @staticmethod
    def get_seller_orders(sid):
        row = app.db.execute("""
SELECT Purchases.id, Purchases.uid, Users.email, Users.address, Products.name, Purchases.quantity, Purchases.time_purchased, Purchases.order_status
FROM Purchases
INNER JOIN Users
ON Purchases.uid = Users.id
INNER JOIN Products
ON Purchases.pid = Products.id
WHERE Purchases.sid = :sid
ORDER BY Purchases.time_purchased DESC
""",
            sid = sid)
        return row

    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT Sells.id, uid, pid, quantity, CONCAT(Users.firstname, \' \', Users.lastname) as name
FROM Sells, Users
WHERE pid = :pid AND Sells.uid = Users.id
''',
                              pid=pid)
        return rows if rows else None

    
    #similar method, but when a search term is specified, limit to things like search term
    @staticmethod
    def get_limited_seller_orders(sid, entry):
        row = app.db.execute("""
SELECT Purchases.id, Purchases.uid, Users.email, Users.address, Products.name, Purchases.quantity, Purchases.time_purchased, Purchases.order_status
FROM Purchases
INNER JOIN Users
ON Purchases.uid = Users.id
INNER JOIN Products
ON Purchases.pid = Products.id
WHERE Purchases.sid = :sid
AND Products.name LIKE :entry
ORDER BY Purchases.time_purchased DESC
""",
            sid = sid,
            entry = '%' + entry + '%')
        return row
            
    @staticmethod
    def fulfillorder(id):
        fulfill = "True"
        row = app.db.execute("""
UPDATE Purchases
SET order_status = :fulfill
WHERE id = :id
""",
            id = id, fulfill=fulfill)
        return row
        