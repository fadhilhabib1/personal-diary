import os
import requests
from bs4 import BeautifulSoup
from os.path import join, dirname
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DEEPAI_URI = os.environ.get("DEEPAI_URI")

client = MongoClient(MONGODB_URI)

db = client.dbdiary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title']
    description_receive = request.form['description']
    date_receive = request.form['date']

    if title_receive == "":
        return jsonify({'msg':'you must provide a title'})
    elif description_receive == "":
        return jsonify({'msg':'you must provide a description'})
    else:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        req = requests.get(DEEPAI_URI+title_receive, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        image = soup.select_one('img')
        src = image.get('src')
        doc = {
            'image': src,
            'title': title_receive,
            'description': description_receive,
            'dates' : date_receive,
        }
        db.diary.insert_one(doc)

        return jsonify({'msg':'posting successful'})

@app.route('/diary', methods=["GET"])
def show_diary():
    sample_receive = list(db.diary.find({}, {'_id': False}))
    return jsonify({'diarys': sample_receive})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)