import json
import math
from flask import Flask, render_template, url_for, request, redirect, jsonify
from pymongo import MongoClient
import cv2
import numpy as np
from model import getSimilarImages

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


@app.route('/image-search', methods=['POST'])
def imageSearch():
    if 'image' not in request.files:
        return jsonify({'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'No image selected for uploading'})

    similar_products = []
    if file and allowed_file(file.filename):
        image = read_image_as_array(file)
        similar_images, distance, filenames = getSimilarImages(image)

        found_images_filenames = []
        for i in range(5):
            if distance[0][i] < 0.8:
                found_images_filenames.append(filenames[int(similar_images[i])])

        found_images_id = []
        for filename in found_images_filenames:
            found_images_id.append(int(filename.split('\\')[1].split('.')[0]))

        similar_products = list(products.find({"ProductId": {'$in': found_images_id}}))

    return json.dumps(similar_products, default=str)


def read_image_as_array(image):
    # Read the image file as a NumPy array
    np_arr = np.frombuffer(image.read(), np.uint8)
    image_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image_array


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
