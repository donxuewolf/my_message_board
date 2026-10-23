from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. 配置 SQLite 数据库，文件会保存在本地名为 site.db 的文件中
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 2. 定义数据库模型（相当于在数据库里建一张留言表）
class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)  # 唯一编号（主键）
  content = db.Column(db.String(500), nullable=False)  # 留言内容，最长500字符


# 自动创建数据库表
with app.app_context():
  db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    user_msg = request.form.get('content')
    if user_msg:
      # 3. 把新留言存入数据库
      new_message = Message(content=user_msg)
      db.session.add(new_message)
      db.session.commit()
    return redirect(url_for('home'))

  # 4. 从数据库中查询所有的留言
  messages = Message.query.all()
  return render_template('index.html', messages=messages)


if __name__ == '__main__':
  app.run(debug=True)