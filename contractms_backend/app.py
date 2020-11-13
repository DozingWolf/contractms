from flask import Flask,make_response,jsonify,abort,request
from flask_httpauth import HTTPBasicAuth

dataset = [{'name':"CSY",'age':30},{'name':"WCY",'age':"25"}]

app = Flask(__name__)

@app.route('/Goodjob')
def index():
    return "Hello!World!GoodJob！"

@app.route('/')
def mainpage():
    return "This is a main page"

@app.route('/api/v1.0/getallemp',methods=['GET'])
def getallemployee():
    return jsonify(dataset)

#一个标准的get方法，使用？传递参数
@app.route('/api/v1.0/testget',methods=['GET'])
def getemp():
    if request.args is None:
        return abort(501)
    internaldata = request.args.to_dict()
    empname = internaldata.get('empname')
    return jsonify(empname)

#不同的get方法，使用自定义的方式传递参数
@app.route('/api/v1.0/emp/getemployeedetail/<string:empname>',methods=['GET'])
def getemployee(empname):
    for user in dataset:
        if user['name'] == empname:
            return jsonify(user['age'])
        else:
            pass

@app.errorhandler(404)
def pagenotfound(error):
    return make_response(jsonify({'error':'PAGE NOT FOUND!'}),404)
@app.errorhandler(501)
def internalerror(error):
    return make_response(jsonify({'error':'INTERNAL ERROR!'}),501)
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
