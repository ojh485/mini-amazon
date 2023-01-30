from flask import current_app as app


class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, id, uid, pid, stars, review, time_reviewed):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.stars = stars
        self.review = review
        self.time_reviewed = time_reviewed

    #Basic Retrieval
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT Products.id, name, price, available, category, description, product_page, image, ROUND(AVG(stars), 2) as average
FROM Products, Reviews
WHERE Products.id = :id AND Products.id = pid
GROUP BY Products.id
''',
                              id=id)
        return rows[0] if rows is not None else None

    #Get by UID
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT DISTINCT Reviews.id, Reviews.uid, Reviews.pid, stars, review, time_reviewed, Products.name as name
FROM Reviews, Products, Purchases
WHERE Reviews.uid = :uid
AND Products.id = Reviews.pid
AND Reviews.pid = Purchases.pid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return rows


    #Get by UID Since
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, stars, review, time_reviewed
FROM Reviews
WHERE uid = :uid
AND time_reviewed >= :since
ORDER BY time_reviewed DESC
''',
                              uid=uid,
                              since=since)
        return [Review(*row) for row in rows]


    #SQL Query to Get Product Average
    @staticmethod
    def get_product_avg(pid):
        rows = app.db.execute('''
SELECT ROUND(AVG(stars), 2) as average
FROM Reviews
WHERE pid = :pid
''',
                              pid=pid)
        average = rows[0][0]
        return average

    #SQL Query to Get Count
    @staticmethod
    def get_product_count(pid):
        rows = app.db.execute('''
SELECT COUNT(id)
FROM Reviews
WHERE pid = :pid
''',
                              pid=pid)
        count = rows[0][0]
        return count

    #SQL Query to Get Product Reviews
    @staticmethod
    def get_product_reviews(pid):
        rows = app.db.execute('''
SELECT id, uid, pid, stars, review, time_reviewed
FROM Reviews
WHERE pid = :pid
''',
                              pid=pid)
        return rows


    #SQL Query to Write Review
    @staticmethod
    def write_review(uid, pid, stars, review, time_reviewed):
        rows = app.db.execute("""
INSERT INTO Reviews(uid, pid, stars, review, time_reviewed)
VALUES(:uid, :pid, :stars, :review, :time_reviewed)
RETURNING id
""",
                                  uid = uid,
                                  pid = pid, stars = stars, review = review, time_reviewed = time_reviewed)
                            

    #SQL Query to Check if Review Exists
    @staticmethod
    def check_review(uid, pid):
        rows = app.db.execute("""
SELECT uid, pid
FROM Reviews
WHERE uid = :uid AND pid = :pid
""",
                              uid=uid, pid = pid)
        return len(rows) > 0

    #SQL Query to Show Recent 10 Reviews
    def recent_10(id):
        rows = app.db.execute('''
SELECT id, uid, pid, stars, review, time_reviewed
FROM Reviews
WHERE uid = :uid
ORDER BY time_reviewed DESC
LIMIT 10
''',
                              id=id)
        return Review(*(rows[0])) if rows else None

    #SQL Query to Check if User has Purchased Product
    @staticmethod
    def check_purchase(uid, pid):
        rows = app.db.execute("""
SELECT uid, pid
FROM Purchases
WHERE uid = :uid AND pid = :pid
""",
                              uid=uid, pid = pid)
        return not (len(rows) > 0)

    #SQL Query to Update Review
    @staticmethod
    def update_review(uid, pid, stars, review, time_reviewed):
        rows = app.db.execute("""
    UPDATE Reviews
    SET stars = :stars, review = :review, time_reviewed = :time_reviewed
    WHERE uid = :uid AND pid = :pid
    """,
                              uid=uid, pid = pid, stars = stars, review = review, time_reviewed = time_reviewed)

    
    #SQL Query to Delete Review
    @staticmethod
    def delete_review(uid, pid):
        rows = app.db.execute("""
DELETE FROM Reviews
WHERE uid = :uid AND pid = :pid
""",
                              uid=uid, pid = pid)
        return None
 


    

    
