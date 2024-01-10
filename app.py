import math

from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDb Client
client = MongoClient('localhost', 27017)
# MongoDB database
db = client.serenova
# MongoDB products collection/table
products = db.products


@app.route('/')
def home():
    featured_products = products.find({"ProductId": {"$in": [5467, 24835, 17846]}})
    return render_template('index.html', featured_products=featured_products)


@app.route('/shop-single/<int:pid>')
def shopSingle(pid):
    product = products.find_one({"ProductId": pid})

    random_related_pipeline = [
        {"$match": {"SubCategory": product['SubCategory'], "Gender": {"$ne": "Women"}}},
        {"$sample": {"size": 12}}
    ]
    related_products = list(products.aggregate(random_related_pipeline))

    return render_template('shop-single.html', product=product, related_products=related_products)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shop')
def shop():
    CATEGORIES = [
        "Sports Shoes", "Skirts", "Leggings", "Shirts", "Flip Flops",
        "Clothing Set", "Jackets", "Sandals", "Trousers", "Churidar",
        "Sports Sandals", "Booties", "Innerwear Vests", "Formal Shoes",
        "Shorts", "Rompers", "Tops", "Waistcoat", "Casual Shoes", "Kurtas",
        "Capris", "Blazers", "Jeans", "Heels", "Flats", "Salwar",
        "Lehenga Choli", "Tshirts", "Dresses", "Kurta Sets", "Sweatshirts"
    ]
    PRODUCT_PER_PAGE = 24

    page = request.args.get('page', 1, type=int)
    subcategory = request.args.get('category', 'Sports Shoes', type=str)

    skipCount = PRODUCT_PER_PAGE * (page - 1)
    products_page = products.find({"ProductType": subcategory}).skip(skipCount).limit(PRODUCT_PER_PAGE)

    productCount = products.count_documents({"ProductType": subcategory})
    pageCount = math.ceil(productCount / PRODUCT_PER_PAGE)

    print(pageCount)

    return render_template(
        'shop.html', products=products_page, categories=CATEGORIES,
        checked_cat=subcategory, pageCount=pageCount, currentPage=page, productCount=productCount
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
