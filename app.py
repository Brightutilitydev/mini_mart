#!/usr/bin/env python3
"""Test Flask uploading"""

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'assets')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

products = []


@app.route('/', methods=['GET'])
def index():
    return render_template('upload_product.html')


@app.route('/', methods=['POST'])
def upload_product():
    product_name = request.form.get('product_name')
    brand = request.form.get('brand')
    size = request.form.get('size')
    price = request.form.get('price')
    description = request.form.get('description')

    image_files = request.files.getlist('images[]')

    saved_files = []
    for file in image_files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            saved_files.append(f"assets/{filename}")

    products.append({
        "name": product_name,
        "brand": brand,
        "size": size,
        "price": float(price) if price else 0.0,
        "description": description,
        "images": saved_files
    })

    return redirect(url_for('retrieve'))


@app.route('/uploaded', methods=['GET'])
def retrieve():
    return render_template('gallery.html', products=products)


if __name__ == "__main__":
    app.run(debug=True)
