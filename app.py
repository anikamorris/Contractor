from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

@app.route('/')
def products_index():
    """Show all products."""
    return render_template('products_index.html')