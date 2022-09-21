from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

mongoclient = MongoClient()

client = MongoClient('mongodb+srv://test:sparta@cluster0.yudx8gg.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta_toy

@app.route('/')
def home():
   return render_template('login_page.html')

@app.route('/signUp/')
def signUp():
   return render_template('signUp_page.html')

@app.route('/main/')
def main():
   return render_template('main_page.html')

@app.route('/write/')
def write():
   return render_template('write_page.html')

@app.route('/writeUrl/')
def writeUrl():
   return render_template('write_page_url.html')

@app.route("/write/write", methods=["POST"])
def write_post():
        url_receive = request.form['url_give']
        title_receive = request.form['title_give']
        comment_receive = request.form['comment_give']
        day_receive = request.form['day_give']

        write_list = list(db.contents.find({},{'_id':False}))
        last_var = write_list[-1]
        last_count = last_var['num']
        count = last_count + 1

        doc = {
             'num':count,
             'url':url_receive,
             'title': title_receive,
             'comment':comment_receive,
             'day': day_receive
        }
        db.contents.insert_one(doc)
        return jsonify({'msg': '저장 완료!'})

@app.route("/write/write", methods=["GET"])
def write_get():
    write_list = list(db.contents.find({}, {'_id': False}))
    return jsonify({'contents':write_list})

@app.route("/write/delete", methods=["POST"])
def write_delete():
    num_receive = request.form['num_give']  # 클라이언트에서 숫자값을 받아와도 다 문자로 받음
    db.contents.delete_one({'num': int(num_receive)})  # 문자로 받아온 것을 숫자로 바꿔줘야 함. int 함수 사용

    return jsonify({'msg': '삭제 완료!'})

db.users.delete_one({'name':'bobby'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)