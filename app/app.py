from flask import Flask, flash, abort, Blueprint, request, render_template, session, g, redirect, url_for, escape, jsonify
from utils import *
import json
import random
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api
cloudinary_config = cloudinary.config(cloud_name='climatempo', api_secret='WwH6HWQ0ALwhlrphu4zD9RRQ37I', api_key='689443847436934')

app = Flask(__name__, static_folder=r"templates/static")
app.secret_key = "d9K2ja@cm1v$"

def uploadImage(image):
    identifier_upload = str(uuid.uuid4())
    cloudinary.uploader.upload(image, public_id=identifier_upload)
    srcURL = cloudinary.CloudinaryImage(identifier_upload).build_url()
    return srcURL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/one', methods=['GET', 'POST'])
def one():
    if request.method == 'POST':
        id_batch_db = insert_batch(name = request.form['titulo'], description = request.form['descripcion'])
        session['evento'] = id_batch_db
        session['step'] = '1'
        return redirect(url_for('two'))
        # return jsonify(request.form.to_dict())
    else:
        return render_template('one.html')

@app.route('/two', methods=['GET', 'POST'])
def two():
    if request.method == 'POST':
        emails_raw = request.form['emails']
        email_list = emails_raw.replace('\n', ',').strip().replace(',', ' ').split()
        insert_emails_list(email_list)
        sent_list = [(int(session['evento']), x) for x in email_list]
        insert_sent_list(sent_list)
        session['step'] = '2'
        return redirect(url_for('three'))
    else:
        return render_template('two.html')

@app.route('/three', methods=['GET', 'POST'])
def three():
    if request.method == 'POST':
        images_metadata = {}
        if 'photos' in request.files:
            images_metadata["images"] = []
            for f in request.files.getlist('photos'):
                image_url = uploadImage(f)
                images_metadata["images"].append(image_url)
        insert_images(images = json.dumps(images_metadata), id_batchs = int(session['evento']))
        session['step'] = '3'
        return redirect(url_for('four'))
    else:
        return render_template('three.html')

@app.route('/four', methods=['GET'])
def four():
    id_batchs = int(session['evento'])
    data_batch = get_batch_metadata(id_batchs)
    data_emails = get_emails_to_send(id_batchs)
    return render_template('four.html', data_batch=data_batch, data_emails=data_emails)

@app.route('/detail', methods=['GET'])
def detail():
    id_batchs = int(session['evento'])
    deploy_nfts(id_batchs)
    data_hashes = get_emails_and_txhash(id_batchs)
    return render_template('detail.html', data_hashes=data_hashes)

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    nfts_data = None
    email = None
    wallet = None
    if request.method == 'POST':
        email = request.form['email']
        wallet, nfts_data = get_nfts(email)
    return render_template('wallet.html', nfts_data=nfts_data, email=email, wallet=wallet)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')