from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

# DBが無ければ作成
dname = 'sleep.sqlite3'
#conn = sqlite3.connect(dname)
#conn.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dname
db = SQLAlchemy(app)
db.init_app(app)

# テーブル定義
class SleepingDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sleeping_time = db.Column(db.Integer, nullable=False)
    tablename = '__sleeping__'

# スコア計算
def score():
    return

# 偏差値計算
def deviation():
    return

# データ受取時の処理
@app.route('/score', methods=['POST'])
def post():
    if request.method == 'POST':
        sleeping_int = request.form['sleeping_time']
        if sleeping_int == '':
            return {404, 'not found'}
        d = SleepingDB(sleeping_time=sleeping_int)
        db.session.add(d)
        db.session.commit()

        return sleeping_int

if __name__ == "__main__":
    app.run(debug=True)