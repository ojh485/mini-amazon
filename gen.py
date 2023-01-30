from werkzeug.security import generate_password_hash
import csv
import random 
from faker import Faker

num_users = 1000
num_products = 2000
num_sells = 2000
num_purchases = 3000
num_carts = 5000
num_reviews = 2000
num_ratings = 2000

Faker.seed(0)
fake = Faker()
random.seed(0)


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = str(uid) + profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address']
            dollars = random.randint(1,1000)
            cents = random.randint(0,99)/100
            balance = dollars + cents
            writer.writerow([uid, email, password, firstname, lastname, address, balance])
        print(f'{num_users} generated')
    return

categories = ['Home & Kitchen', 'Beauty & Personal Care', 'Toys & Games', 'Clothing, Shoes & Jewelry',
'Health, Household & Baby Care', 'Sports & Outdoors', 'Arts, Crafts & Sewing', 'Books', 'Kitchen & Dining', 'Electronics']
def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=100))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            category = categories[random.randint(0,len(categories) - 1)]
            description = fake.sentence(nb_words=6)[:-1]
            product_page = fake.image_url()
            image = fake.image_url()
            writer.writerow([pid, name, price, available, category, description, product_page, image])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_sells(num_sells, available_pids):
    sells_combos = []
    with open('Sells.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sells...', end=' ', flush=True)
        for id in range(num_sells):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            if id >= len(available_pids):
                index = id % len(available_pids)
            else:
                index = id
            pid = available_pids[index]
            quantity = fake.random_int(min=10, max=30)
            writer.writerow([id, uid, pid, quantity])
            sells_combos.append([uid, pid])
        print(f'{num_sells} generated')
    return sells_combos

def gen_purchases(num_purchases, sells_combos):
    purchases = []
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            combo = fake.random_element(elements=sells_combos)
            sid = combo[0]
            pid = combo[1]
            quantity = fake.random_int(min=1, max=5)
            time_purchased = fake.date_time()
            item_status = fake.random_element(elements=['true', 'false'])
            order_status = item_status
            writer.writerow([id, uid, pid, sid, quantity, time_purchased, item_status,
                             order_status])
            purchases.append([uid, pid])
        print(f'{num_purchases} generated')
    return purchases

def gen_carts(num_carts, sells_combos):
    print(sells_combos)
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for id in range(num_carts):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            combo = fake.random_element(elements=sells_combos)
            sid = combo[0]
            pid = combo[1]
            quantity = fake.random_int(min=1, max=5)
            writer.writerow([id, uid, pid, sid, quantity])
        print(f'{num_carts} generated')
    return

def gen_reviews(num_reviews, available_purchases):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = available_purchases[id][0]
            pid = available_purchases[id][0]
            stars = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=15)[:-1]
            time_reviewed = fake.date_time()
            writer.writerow([id, uid, pid, stars, review, time_reviewed])
        print(f'{num_reviews} generated')
    return

def gen_ratings(num_ratings):
    with open('Ratings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Ratings...', end=' ', flush=True)
        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            pair = random.sample(range(0, num_users), 2)
            uid = pair[0]
            sid = pair[1]
            stars = fake.random_int(min=1, max=5)
            rating = fake.sentence(nb_words=15)[:-1]
            time_reviewed = fake.date_time()
            writer.writerow([id, uid, sid, stars, rating, time_reviewed])
        print(f'{num_ratings} generated')
    return



def gen_mp_reviews(num_products):
    with open('MP_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_products):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            pid = id
            id = id + 2000
            uid = -1
            stars = 5
            review = 'Marketplace loves your product!'
            time_reviewed = fake.date_time()
            writer.writerow([id, uid, pid, stars, review, time_reviewed])
        print(f'{num_products} generated')
    return

gen_mp_reviews(num_products)