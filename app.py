from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import requests
import json

app = Flask(__name__)

if "MONGODB_URI" in os.environ:
    host = os.environ.get('MONGODB_URI')
else:
    host = "mongodb://localhost:27017/Contractor"
client = MongoClient(host=f'{host}retryWrites=false')
db = client.Contractor
nail_polishes = db.nail_polishes
reviews = db.reviews

@app.route('/')
def products_index():
    """Show all products."""
    # make a request to the makeup api for all nail polish products
    r = requests.get("http://makeup-api.herokuapp.com/api/v1/products.json?product_type=nail_polish")

    # turn the request into json data
    json_data = r.json()
    # only insert products into the database if it's empty
    if nail_polishes.count({}) == 0:
        for nail_polish in json_data:
            nail_polishes.insert_one(nail_polish)

    return render_template('products_index.html', nail_polishes=nail_polishes.find())

# https://gist.github.com/matthewkremer/3295567
# Thank you, Matthew Kremer!
def hex_to_rgb(hex):
    """Turn hex value to rgb value"""
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

@app.route('/products/<product_id>')
def products_show(product_id):
    """Show product with id product_id"""
    # find the one nail polish with _id product_id
    nail_polish = nail_polishes.find_one({'_id': ObjectId(product_id)})
    # initialize empty list to hold nail polish colors
    colors = []
    # loop through the product colors
    for color in nail_polish["product_colors"]:
        # initialize rgb variable with translated hex value
        rgb = hex_to_rgb(color["hex_value"])
        # add a list of the rgb value and color name to colors list
        colors.append([rgb, color["colour_name"]])
    return render_template('products_show.html', nail_polish=nail_polish, colors=colors)

# @app.route('/products/reviews', methods=['POST'])
# def reviews_new():
#     """Submit a new review."""
#     return 'review here'
    # review = {
    #     'title': request.form.get('title'),
    #     'content': request.form.get('content'),
    #     'nail_polish_id': ObjectId(request.form.get('nail_polish_id'))
    # }
    # print(review)
    # review_id = reviews.insert_one(review).inserted_id
    # return redirect(url_for('products_show', product_id=request.form.get('nail_polish_id')))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5002))