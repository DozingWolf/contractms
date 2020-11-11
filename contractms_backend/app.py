from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

@app.route('/Goodjob')
def index():
    return "Hello!World!GoodJob！"

@app.route('/')
def mainpage():
    return "This is a main page"

# flask路由编写案例
# @app.route('/api/users', methods=['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400)  # missing arguments
#     if User.query.filter_by(username=username).first() is not None: #此处使用post的参数进行sqlalchema查询
#         abort(400)  # existing user
#     user = User(username=username) #此处实例化一个User对象，并初始化赋予post进来的用户名
#     user.hash_password(password) #计算哈希后的密码
#     db.session.add(user) #数据通过ORM数据模型写入
#     db.session.commit() #提交数据到数据库
#     return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}

if __name__ == '__main__':
    app.run(debug=True)
