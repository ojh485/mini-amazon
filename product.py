from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, category, description, product_page, image):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.category = category
        self.description = description
        self.product_page = product_page
        self.image = image


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

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
LIMIT 50
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_most_expensive(k):
        rows = app.db.execute('''
SELECT *
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                            k = k)
        return [Product (*row) for row in rows]

    @staticmethod
    def keySearch(key, category, pageNum, sort, minRating, maxPrice):
        rows = app.db.execute('''
SELECT Products.id, name, price, available, category, description, product_page, image, ROUND(AVG(stars), 2) as average
FROM Products, Reviews
WHERE Products.id = Reviews.pid 
AND (name LIKE :key OR description LIKE :key) 
AND (category = :cat OR :cat = 'All')
AND available = 'true'
AND price <= :maxPrice
GROUP BY Products.id
HAVING AVG(stars) >= :minRating
ORDER BY CASE 
    WHEN :sort = 'price' THEN price
    WHEN :sort = 'avg' THEN AVG(stars)
    ELSE Products.id END
OFFSET :pageNum*50
LIMIT 50
''',
                            key = '%' + key + '%',
                            cat = category,
                            pageNum = pageNum - 1,
                            sort = sort,
                            minRating = minRating,
                            maxPrice = maxPrice)
        return rows
    

            
