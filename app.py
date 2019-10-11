from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import requests
import json

app = Flask(__name__)

client = MongoClient()
db = client.Contractor
nail_polishes = db.nail_polishes
cart = db.cart

@app.route('/')
def products_index():
    """Show all products."""
    r = requests.get("http://makeup-api.herokuapp.com/api/v1/products.json?product_type=nail_polish")

    json_data = r.json()
    print('count', nail_polishes.count({}))
    if nail_polishes.count({}) == 0:
        for nail_polish in json_data:
            nail_polishes.insert_one(nail_polish)

    return render_template('products_index.html', nail_polishes=nail_polishes.find())

# https://gist.github.com/matthewkremer/3295567
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

@app.route('/products/<product_id>')
def products_show(product_id):
    nail_polish = nail_polishes.find_one({'_id': ObjectId(product_id)})
    colors = []
    for color in nail_polish["product_colors"]:
        rgb = hex_to_rgb(color["hex_value"])
        colors.append([rgb, color["colour_name"]])
    return render_template('products_show.html', nail_polish=nail_polish, colors=colors)

