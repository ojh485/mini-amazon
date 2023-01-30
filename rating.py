from flask import current_app as app


class Rating:
    """
    This is just a TEMPLATE for Rating, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, id, uid, sid, stars, rating, time_reviewed):
        self.id = id
        self.uid = uid
        self.sid = sid
        self.stars = stars
        self.rating = rating
        self.time_reviewed = time_reviewed

    #Basic Retrieval
    @staticmethod
    def get(id):
        rows = app.db.execute('''

SELECT id, uid, sid, stars, rating, time_reviewed
FROM Ratings
WHERE id = :id
ORDER BY time_reviewed DESC
''',
                              id=id)
        return Rating(*(rows[0])) if rows else None

    #Get by UID Since
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, sid, stars, rating, time_reviewed
FROM Ratings
WHERE uid = :uid
AND time_reviewed >= :since
ORDER BY time_reviewed DESC
''',
                              uid=uid,
                              since=since)
        return [Rating(*row) for row in rows]

    #Get by UID
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT DISTINCT Ratings.id, Ratings.uid, Ratings.sid, stars, rating, time_reviewed, CONCAT(Users.firstname, \' \', Users.lastname) as seller
FROM Ratings, Users, Purchases
WHERE Ratings.uid = :uid
AND Users.id = Ratings.sid 
AND Ratings.sid = Purchases.uid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return rows


    #SQL Query to Get Seller Average
    @staticmethod
    def get_seller_avg(sid):
        rows = app.db.execute('''
SELECT ROUND(AVG(stars), 2) as average
FROM Ratings
WHERE sid = :sid
''',
                              sid=sid)
        average = rows[0][0]
        return average

    #SQL Query to Get Seller Ratings
    @staticmethod
    def get_seller_ratings(sid):
        rows = app.db.execute('''
SELECT id, uid, sid, stars, rating, time_reviewed
FROM Ratings
WHERE sid = :sid
''',
                              sid=sid)
        return [Rating(*row) for row in rows] if rows else []

    #SQL Query to Write Review
    @staticmethod
    def write_rating(id, uid, sid, stars, rating, time_reviewed):
        rows = app.db.execute("""
INSERT INTO Ratings(id, uid, sid, stars, rating, time_reviewed)
VALUES(:id, :uid, :sid, :stars, :rating, :time_reviewed)
RETURNING id
""",
                                  id = id,
                                  uid = uid,
                                  sid = sid, stars = stars, rating = rating, time_reviewed = time_reviewed)
    
    #SQL Query to Get Count
    @staticmethod
    def get_seller_count(sid):
        rows = app.db.execute('''
SELECT COUNT(id)
FROM Ratings
WHERE sid = :sid
''',
                              sid=sid)
        count = rows[0][0]
        return count

    #SQL Query to Write Rating
    @staticmethod
    def write_rating(uid, sid, stars, rating, time_reviewed):
        rows = app.db.execute("""
INSERT INTO Ratings(uid, sid, stars, rating, time_reviewed)
VALUES(:uid, :sid, :stars, :rating, :time_reviewed)
RETURNING id
""",
                                  uid = uid,
                                  sid = sid, stars = stars, rating = rating, time_reviewed = time_reviewed)
                            

    #SQL Query to Check if Rating Exists
    @staticmethod
    def check_rating(uid, sid):
        rows = app.db.execute("""
SELECT uid, sid
FROM Ratings
WHERE uid = :uid AND sid = :sid
""",
                              uid=uid, sid = sid)
        return len(rows) > 0

    #SQL Query to Check if Purchase History Exists
    def check_purchase(uid, sid):
        rows = app.db.execute("""
SELECT uid, sid
FROM Purchases
WHERE uid = :uid AND sid = :sid
""",
                              uid=uid, sid = sid)
        return not (len(rows) > 0)
    
    #SQL Query to Update Rating
    @staticmethod
    def update_rating(uid, sid, stars, rating, time_reviewed):
        rows = app.db.execute("""
    UPDATE Ratings
    SET stars = :stars, rating = :rating, time_reviewed = :time_reviewed
    WHERE uid = :uid AND sid = :sid
    """,
                              uid=uid, sid = sid, stars = stars, rating = rating, time_reviewed = time_reviewed)

    #SQL Query to Delete Rating
    @staticmethod
    def delete_rating(uid, sid):
        rows = app.db.execute("""
DELETE FROM Ratings
WHERE uid = :uid AND sid = :sid
""",
                              uid=uid, sid = sid)
        return None

        