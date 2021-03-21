from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import numpy as np

# DBが無ければ作成
dname = 'sleep.sqlite3'
#conn = sqlite3.connect(dname)
#conn.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

# テーブル定義
class SleepingDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sleeping_time = db.Column(db.Float, nullable=False)
    tablename = '__sleeping__'

# スコア計算
def score_count(sleeping_time):
    score = abs(sleeping_time-7.5)/7.5*100

    return score

# 偏差値計算
def deviation_count(sleeping_time):
    sleeping_times = db.session.query(SleepingDB.sleeping_time).all()
    ave = np.mean(sleeping_times)
    std = np.std(sleeping_times)
    dev = (sleeping_time -ave)/std
    dev_val = 50 + dev*10

    return dev_val

# データ受取時の処理
@app.route('/score', methods=['POST'])
def post():
    if request.method == 'POST':
        sleeping_hour = request.form['sleeping_hour']
        sleeping_minute = request.form['sleeping_minute']
        if sleeping_hour == '' or sleeping_minute== '':
            return {404, 'not found'}
        sleeping_time = float(sleeping_hour) + float(sleeping_minute)/60.0
        d = SleepingDB(sleeping_time=sleeping_time)
        db.session.add(d)
        db.session.commit()

        score = score_count(sleeping_time)
        deviation = deviation_count(sleeping_time)
        deviation = round(deviation, 5)

        if deviation > 55:
            return render_template("gold.html", sleeping_time=sleeping_time, score=score, deviation= deviation)
        if 55 >= deviation >= 50:
            return render_template("silver.html", sleeping_time=sleeping_time, score=score, deviation= deviation)
        else:
            return render_template("copper.html", sleeping_time=sleeping_time, score=score, deviation= deviation)
        #return {'time': sleeping_time, 'score': score, 'deviation': deviation}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)