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
    for nail_polish in json_data:
        db.nail_polishes.insert_one(nail_polish)

    return render_template('products_index.html', nail_polishes=nail_polishes.find())

@app.route('/products/<product_id>')
def products_show(product_id):
    nail_polish = nail_polishes.find_one({'_id': ObjectId(product_id)})
    return render_template('products_show.html', nail_polish=nail_polish)

@app.route('/cart')
def show_cart():
    return render_template('cart.html')