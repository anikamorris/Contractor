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

@app.route('/')
def products_index():
    """Show all products."""
    r = requests.get("http://makeup-api.herokuapp.com/api/v1/products.json?product_type=nail_polish&limit=20")

    json_data = r.json()
    for nail_polish in json_data:
        db.nail_polishes.insert(nail_polish)

    return render_template('products_index.html', nail_polishes=nail_polishes.find())