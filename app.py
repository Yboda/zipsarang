from flask import Flask, render_template
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.um5wee2.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

doc = {
    'test' : 'test'
}

@app.route('/')
def home():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)


    @app.route('/comment', methods=['POST'])
    def comment():

            # 댓글 저장
            return jsonify({"result": "success", 'msg': '저장성공'})



    @app.route("/get_commnet", methods=['GET'])
    def get_posts():

            # 댓글 목록 받아오기
            return jsonify({"result": "success", "msg": "댓글왔다"})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))