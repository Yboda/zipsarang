# flask, pymongo, dnspython, PyJWT 설치
from flask import Flask, render_template, jsonify, request, redirect, url_for

from pymongo import MongoClient
from bson.objectid import ObjectId

import os

from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import jwt


# 회원가입 시, 비밀번호 암호화
import hashlib

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/default_img"

SECRET_KEY = 'zipsarang'


# local
# client = MongoClient('mongodb+srv://test:test@cluster0.um5wee2.mongodb.net/?retryWrites=true&w=majority')
# aws
client = MongoClient('54.180.148.42', 27017, username="test", password="test")
db = client.zipsarang

@app.route('/')
def home():

    postinglist = list(db.posting.find({}))

    for posting in postinglist:
        posting['_id'] = str(posting['_id'])

    user_token = request.cookies.get('user_token')
    try:
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        return render_template('index.html', postinglist=postinglist, user_info=user_info, status=False)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('index.html', postinglist=postinglist, status=True)


@app.route('/sign_up', methods=['GET'])
def go_sing_up():
    user_token = request.cookies.get('user_token')
    try:
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        return redirect(url_for("home"))
#        return render_template('index.html', user_info=user_info, status=False)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('user.html', status=True)

@app.route('/sign_up', methods=['POST'])
def sign_up():

    file = request.files["file"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y%m%d%H%M%S')

    filename = f'file--{mytime}'

    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'

    save_to = f'{dir}static/{filename}.{extension}'
    file.save(save_to)

    user_id = request.form['user_id']
    password = request.form['password']
    nickname = request.form['nickname']
    cat_name = request.form.get('cat_name')
    intro = request.form.get('intro')

    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "user_id": user_id,     # 아이디
        "password": pw_hash,    # 비밀번호
        "nickname": nickname,   # 닉네임
        "cat_name": cat_name,   # 고양이 이름
        "intro": intro,         # 간단한 소개글
        'cat_img': f'{filename}.{extension}'    # 고양이 사진
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    user_id = request.form['user_id']
    exists = bool(db.users.find_one({"user_id": user_id}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/login', methods=['GET'])
def go_login():
    user_token = request.cookies.get('user_token')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # 로그인
    user_id = request.form['user_id']
    password = request.form['password']

    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': user_id, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': user_id,
         'exp': datetime.utcnow() + timedelta(seconds=3600)  # 로그인 1시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/mypage')
def mypage():
    user_token = request.cookies.get('user_token')

    if user_token is not None:
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})

        return render_template('user.html', user_info=user_info, status=False)
    else:
        return redirect(url_for("home"))
        #return render_template('index.html', status=True)

@app.route('/update_user', methods=['POST'])
def update_user():

    original = db.users.find_one({'user_id': request.form['user_id']})

    password = request.form.get('password')
    nickname = request.form.get('nickname')
    cat_name = request.form.get('cat_name')
    intro = request.form.get('intro')

    if password is not None:
        pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        db.users.update_one({'user_id': request.form['user_id']}, {'$set': {'password': pw_hash}})

    if original['cat_img'] != request.form['fileName']:
        file = request.files["file"]

        extension = file.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y%m%d%H%M%S')

        filename = f'file--{mytime}'

        dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'

        save_to = f'{dir}./static/{filename}.{extension}'
        file.save(save_to)

        db.users.update_one({'user_id': request.form['user_id']}, {'$set': {'cat_img': f'{filename}.{extension}'}})

    db.users.update_one({'user_id': request.form['user_id']}, {'$set': {'nickname': nickname, 'cat_name': cat_name, 'intro': intro}})

    return jsonify({'result': 'success'})

@app.route('/default_password', methods=['POST'])
def default_password():

    user_id = request.form.get('user_id')
    cat_name = request.form.get('cat_name')

    find_user = db.users.find_one({"user_id": user_id, "cat_name" : cat_name})
    if find_user is None:
        return jsonify({'msg' : "입력하신 내용과 일치하는 정보가 없습니다."})
    # 비밀번호 mycat123 초기화
    db.users.update_one({'user_id': user_id}, {'$set': {'password': '0e024e5ab7654161d9ee542721aa626a25cbfdb1380e25006afce1e57633ded7'}})

    return jsonify({'msg' : user_id + "의 비밀번호가 'mycat123'으로 변경되었습니다."})

@app.route('/new_posting', methods=['POST'])
def new_posting():

    file = request.files["file"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y%m%d%H%M%S')

    filename = f'file--{mytime}'

    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'

    save_to = f'{dir}static/{filename}.{extension}'
    file.save(save_to)

    user_id = request.form['user_id']
    desc = request.form['desc']
    nickname = request.form['nickname']
    cat_name = request.form.get('cat_name')

    doc = {
        "cat_img": f'{filename}.{extension}',    # 고양이 사진
        "desc": desc,           # 자랑글
        "user_id": user_id,    # 작성자
        "nickname": nickname,   # 닉네임
        "cat_name": cat_name   # 고양이 이름
    }
    db.posting.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/posting_info', methods=['POST'])
def posting_info():
    #포스팅 조회
    _id = request.form['_id']
    posting = db.posting.find_one({'_id' : ObjectId(_id)},{'_id':False})

    comments = list(db.comment.find({'posting_id' : _id}))

    for comment in comments:
        comment['_id'] = str(comment['_id'])

    return jsonify({"posting_info": posting, "comments" : comments})

@app.route('/new_comment', methods=['POST'])
def comment():

    user_id = request.form['user_id']
    posting_id = request.form['posting_id']
    comment = request.form['comment']
    nickname = request.form['nickname']

    doc = {
        "comment" : comment,
        "nickname" : nickname,
        "user_id" : user_id,
        "posting_id" : posting_id
    }

    db.comment.insert_one(doc)

    # 댓글 저장
    return jsonify({"result": "success"})

@app.route("/get_commnet", methods=['GET'])
def get_posts():
    # 댓글 목록 받아오기
    return jsonify({"result": "success", "msg": "댓글왔다"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

