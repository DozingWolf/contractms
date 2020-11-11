from flask import Flask

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
#     if User.query.filter_by(username=username).first() is not None:
#         abort(400)  # existing user
#     user = User(username=username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}

if __name__ == '__main__':
    app.run(debug=True)
