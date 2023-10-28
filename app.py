from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://test:sparta@cluster0.rv9cjgy.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d_%H-%M-%S')
    
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    save_to = f'static/profile/{profilename}'
    profile.save(save_to)

    time = today.strftime('%Y-%m-%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time' : time
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)