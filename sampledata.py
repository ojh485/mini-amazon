#Sample code taken from https://www.pythontutorial.net/python-basics/python-write-csv-file/
import csv

#Sample users
user_cols = ['uid', 'name', 'address', 'email', 'password', 'balance']
user_data = [
    [1, 'Dominic Jeong', '670 Union Ave', 'dominic.jeong@gmail.com', 'passw0rd', 250],
    [2, 'Billy Luqiu', '123 Erwin Rd', 'billyluqiu@yahoo.com', 'dominiciscool', 120],
    [3, 'Luke Thomas', '999 Cameron Blvd', 'lukethomas@gmail.com', 'iplaysoccer', 100],
    [4, 'Phillip Rivers', '1001 Retirement Ave', 'ilovemykids@gmail.com', 'toomanykids', 1000],
    [5, 'Geno Smith', '555 Seahawk Ln', 'genosmith@gmail.com', 'imactuallyokay', 2500],
    [6, 'Russell Wilson', '123 Broncos Country', 'broncoscountry@gmail.com', 'broncoscountryletsride', 1],
    [7, 'Kobe Bryant', '958 Mamba Ave', 'kobeandgigi@gmail.com', 'mambaforever', 2],
    [8, 'Owen Hand', '315 Towerview Dr', 'amazonians@gmail.com', 'amazonians', 3],
    [9, 'Bennett Bierman', '104 Union Dr', 'eggsbenny@gmail.com', 'benny123', 4],
    [10, 'Vivaan Baid', '105 Durham Blvd', 'vivaanbaid@gmail.com', 'vivaan123', 5]
]
with open('sample_users.csv', 'w', encoding = 'UTF8', newline='') as sample_users:
    writer = csv.writer(sample_users)
    writer.writerow(user_cols)
    writer.writerows(user_data)

#Sample sellers
seller_cols = ['uid']
seller_data = [
    [1], [2], [3], [4], [5]
]
with open('sample_sellers.csv', 'w', encoding = 'UTF8', newline='') as sample_sellers:
    writer = csv.writer(sample_sellers)
    writer.writerow(seller_cols)
    writer.writerows(seller_data)

#Sample products
product_cols = ['pid', 'category', 'prod_page', 'name', 'description', 'image', 'price']
product_data = [
    [12345, 'sports', 'website1', 'basketball', 'big basketball', 'image1', 30],
    [12346, 'lifestyle', 'website2', 'sofa', 'big sofa', 'image2', 400],
    [12347, 'sports', 'website3', 'football', 'standard football', 'image3', 30],
    [12348, 'fashion', 'website4', 'romphim', 'male romper', 'image4', 25],
    [12349, 'lifestyle', 'website5', 'mini table', 'small table', 'image5', 50],
    [12350, 'fashion', 'website6', 'socks', 'short socks', 'image6', 10],
    [12351, 'food', 'website7', 'granola bars', 'pack of 12', 'image7', 5]
]
with open('sample_products.csv', 'w', encoding = 'UTF8', newline='') as sample_products:
    writer = csv.writer(sample_products)
    writer.writerow(product_cols)
    writer.writerows(product_data)

#Sample carts
cart_cols = ['sellerid', 'buyerid', 'pid', 'quantity']
cart_data = [
    [1, 6, 12346, 1],
    [2, 7, 12345, 10],
    [3, 8, 12350, 3],
    [4, 9, 12348, 5],
    [5, 10, 12347, 2]
]
with open('sample_carts.csv', 'w', encoding = 'UTF8', newline='') as sample_carts:
    writer = csv.writer(sample_carts)
    writer.writerow(cart_cols)
    writer.writerows(cart_data)

#Sample orders
orders_cols = ['buyerid', 'sellerid', 'pid', 'time', 'quantity', 'item_status', 'order_status', 'order_page']
orders_data = [
    [1, 7, 12345, '01:00:49', 2, 'in stock', 'shipped', 'website1'],
    [2, 6, 12348, '02:10:00', 3, 'out of stock', 'waiting', 'website2'],
    [3, 10, 12350, '03:00:00', 1, 'in stock', 'shipped', 'website3'],
    [4, 8, 12347, '04:00:49', 5, 'in stock', 'delivered', 'website4'],
    [5, 9, 12346, '05:00:49', 3, 'in stock', 'delivered', 'website5']
]
with open('sample_orders.csv', 'w', encoding = 'UTF8', newline='') as sample_orders:
    writer = csv.writer(sample_orders)
    writer.writerow(orders_cols)
    writer.writerows(orders_data)

#Sample sell listings
sell_cols = ['uid', 'pid', 'quantity']
sell_data = [
    [1, 12345, 10],
    [1, 12346, 2],
    [2, 12345, 10],
    [2, 12348, 2],
    [3, 12350, 5],
    [4, 12348, 6],
    [4, 12347, 6],
    [5, 12347, 3],
    [5, 12346, 5]
]
with open('sample_sells.csv', 'w', encoding = 'UTF8', newline='') as sample_sells:
    writer = csv.writer(sample_sells)
    writer.writerow(sell_cols)
    writer.writerows(sell_data)

#Sample product reviews
review_cols = ['uid', 'pid', 'stars', 'description', 'time']
review_data = [
    [6, 12346, 5, "great", "00:00:00"],
    [7, 12348, 2, "trash", "03:50:00"],
    [8, 12347, 5, "amazing", "10:30:07"],
    [9, 12349, 4, "pretty good", "14:12:49"],
    [10, 12350, 1, "horrible", "10:10:10"]
]
with open('sample_reviews.csv', 'w', encoding = 'UTF8', newline='') as sample_reviews:
    writer = csv.writer(sample_reviews)
    writer.writerow(review_cols)
    writer.writerows(review_data)

#Sample seller ratings
rating_cols = ['buyerid', 'sellerid', 'stars', 'description', 'time']
rating_data = [
    [6, 1, 5, "good job", "10:00:00"],
    [7, 2, 2, "horrible", "03:30:05"],
    [8, 3, 5, "phenomenal", "11:32:09"],
    [9, 4, 4, "good", "19:11:46"],
    [10, 5, 1, "god awful", "11:11:11"]
]
with open('sample_ratings.csv', 'w', encoding = 'UTF8', newline='') as sample_ratings:
    writer = csv.writer(sample_ratings)
    writer.writerow(rating_cols)
    writer.writerows(rating_data)


