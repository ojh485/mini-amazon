from flask import current_app as app
from datetime import datetime


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None


    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_recommendations(uid):
        rows = app.db.execute('''
SELECT id, name, description, price, image, category
FROM (SELECT Products.id, Products.name, Products.description, Products.price, Products.image, Products.category, COUNT(*) as total
FROM Purchases, Products
WHERE Purchases.pid = Products.id AND Products.category IN (SELECT category
FROM (SELECT Products.category, COUNT(Products.id) AS total
FROM Purchases, Products
WHERE Purchases.pid = Products.id AND Purchases.uid = :uid
GROUP BY Products.category) AS T
ORDER BY T.total DESC
LIMIT 1)
GROUP BY Products.id, Products.name, Products.category, Products.description, Products.image, Products.price) AS A
ORDER BY A.total DESC
LIMIT 5
''',
                              uid=uid)
        return rows

    
    
    

    
    @staticmethod
    def get_purchase_history(uid, category, search):
        if category == 'Item' and len(search) > 0:
            rows = app.db.execute('''
    SELECT total, name, quantity, item_status, time_purchased, sid
    FROM (
        SELECT quantity*price AS total, quantity, item_status, time_purchased, uid, sid, name 
        FROM Purchases, Products
        WHERE Purchases.pid = Products.id
    ) AS T
    WHERE uid = :uid AND name LIKE '%' || :search || '%'
    ORDER BY time_purchased DESC
    ''',
                                uid=uid, search=search)
            return rows
        
        elif category == 'Date':
            try:
                test = datetime.strptime(search, f'%Y-%m-%d %H:%M:%S')
                rows = app.db.execute('''
        SELECT total, name, quantity, item_status, time_purchased, sid
        FROM (
            SELECT quantity*price AS total, quantity, item_status, time_purchased, uid, sid, name 
            FROM Purchases, Products
            WHERE Purchases.pid = Products.id
        ) AS T
        WHERE uid = :uid AND time_purchased = :search
        ORDER BY time_purchased DESC
        ''',
                                    uid=uid, search=search)
                return rows
            except ValueError as ve:
                print(ve)
                return []
        elif category == 'Delivered' and (search.lower() == 'true' or search.lower() == 'false'):
            rows = app.db.execute('''
    SELECT total, name, quantity, item_status, time_purchased, sid
    FROM (
        SELECT quantity*price AS total, quantity, item_status, time_purchased, uid, sid, name 
        FROM Purchases, Products
        WHERE Purchases.pid = Products.id
    ) AS T
    WHERE uid = :uid AND item_status = :search
    ORDER BY time_purchased DESC
    ''',
                                uid=uid, search=search)
            return rows
        elif category == 'All':
            rows = app.db.execute('''
    SELECT total, name, quantity, item_status, time_purchased, sid
    FROM (
        SELECT quantity*price AS total, quantity, item_status, time_purchased, uid, sid, name 
        FROM Purchases, Products
        WHERE Purchases.pid = Products.id
    ) AS T
    WHERE uid = :uid
    ORDER BY time_purchased DESC
    ''',
                                uid=uid)
            return rows
        
        else:
            return []


    
    @staticmethod
    def get_seller_history(uid):
        rows = app.db.execute('''
SELECT total, name, quantity, item_status, time_purchased, sid
FROM (
    SELECT quantity*price AS total, quantity, item_status, time_purchased, uid, sid, name 
    FROM Purchases, Products
    WHERE Purchases.pid = Products.id
) AS T
WHERE sid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return rows
    

    # Find a users most popular product category and recommend the most popular
    # products in that category
    @staticmethod
    def getProfits(uid):
        rows = app.db.execute('''
((SELECT quantity*price AS weighted_price, time_purchased
FROM Purchases, Products
WHERE sid =:uid AND Purchases.pid = Products.id)
UNION
(SELECT quantity*price*-1 AS weighted_price, time_purchased
FROM Purchases, Products
WHERE uid =:uid AND Purchases.pid = Products.id))
ORDER BY time_purchased ASC
''',
                              uid=uid)
        return rows
