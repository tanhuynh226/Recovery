from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from user import *
from barcode_reader import *
import requests
from PIL import Image
import io

app = Flask("server")

@app.route('/calculate/initial', methods=['POST'])
def calculate_initial():
    user = request.json
    nutrients = calculate_initial_nutrients(user)
    return jsonify(nutrients)

@app.route('/item/barcode', methods=['GET'])
def get_barcode_data():
    # This receives a raw image data url. Look to Pillow documentation for specific parsing instructions.
    imgurl = request.args.get('imgurl')
    img = Image.open(requests.get(imgurl, stream=True).raw)
    barcode_info = get_barcode_info(img)
    return jsonify(barcode_info)

@app.route('/item/barcode/id', methods=['GET'])
def get_product_data():
    barcode_id = request.args.get('query')
    product_info = get_product_info(barcode_id)
    return jsonify(product_info)

@app.route('/item/search', methods=['GET'])
def search():
    item = request.args.get('query')
    item_list = search_items(item)
    return item_list.json()

@app.route('/item/add', methods=['POST'])
def add_item():
    food = request.json['food']
    nutrients = request.json['nutrients']
    if food['type'] == "barcode":
        nutrients = add_item_barcode(food['id'], nutrients)
    elif food['type'] == "fdcid":
        nutrients = add_item_fdcid(food['id'], nutrients)
    return jsonify(nutrients)

@app.route('/item/delete', methods=['POST'])
def delete_item():
    food = request.json['food']
    nutrients = request.json['nutrients']
    if food['type'] == "barcode":
        nutrients = delete_item_barcode(food['id'], nutrients)
    elif food['type'] == "fdcid":
        nutrients = delete_item_fdcid(food['id'], nutrients)
    return jsonify(nutrients)