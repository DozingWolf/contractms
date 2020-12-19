from flask import Flask,make_response,jsonify,abort,request,json
from flask_httpauth import HTTPBasicAuth
from configparser import ConfigParser
import logging
import base64
import cx_Oracle
import os
from urllib.parse import urlencode
from base import AppInitial

mainDB = AppInitial()
dbConn,mainLog = mainDB.getMainFunc()
dbCurs = dbConn.cursor()

app = Flask(__name__)

#标准get方法，使用？进行传参
@app.route('/api/v1.0/getuser/',methods=['GET'])
def getuser():
    # 此处的判断空参数好像没有起作用？以后研究以下。。。
    if request.args is None:
        return abort(501)
    query_conditions = request.args.to_dict()
    mainLog.debug('get parameter is :%s'%query_conditions)
    try:
        usercode = query_conditions.get('usercode')
        mainLog.debug(type(usercode),usercode)
        username = query_conditions.get('username')
    except Exception as err:
        mainLog.error('there is a error in get parament :%s'%err)
    select_it_mst_users = ''
    select_it_mst_users_base = '''
    select
    USERCODE, USERNAME, USERPW
    from it_mst_users
    where 1=1
    and stopflag = '00'
    '''

    select_it_mst_user_arg_set = {}
    # 判断usercode是否为空
    if query_conditions.get('usercode',-1) != -1:
        select_it_mst_users = select_it_mst_users_base + 'and usercode =:usercode '
        select_it_mst_user_arg_set.update({'usercode':usercode})
    else:
        select_it_mst_users = select_it_mst_users_base

    # 判断username是否为空
    if query_conditions.get('username',-1) != -1:
        select_it_mst_users = select_it_mst_users + 'and username =:username'
        select_it_mst_user_arg_set.update({'username':username})

    # 判断所有参数是否都为空
    if not bool(select_it_mst_user_arg_set):
        mainLog.error('no input parameter')
        return abort(503)
    
    try:
        dbCurs.execute(select_it_mst_users,select_it_mst_user_arg_set)
        mainLog.debug('execute sql success %s'%select_it_mst_users)
        mainLog.debug('sql arg : %s'%select_it_mst_user_arg_set)
        dbResult = dbCurs.fetchall()
        mainLog.debug('result is : %s'%dbResult)
    except Exception as err:
        mainLog.error('execute sql error : %s'%err)
        mainLog.error('sql : %s'%select_it_mst_users)
        mainLog.error('sql arg : %s'%select_it_mst_user_arg_set)
    #local_rst_set = json.dumps([dbResult[0][0],dbResult[0][1]])
    local_rst_set = json.dumps(dbResult)
    print(local_rst_set)
    return make_response(local_rst_set)

@app.route('/Goodjob')
def index():
    return "Hello!World!GoodJob！"

@app.route('/')
def mainpage():
    return "This is a main page"

@app.route('/api/v1.0/getallemp',methods=['GET'])
def getallemployee():
    return jsonify('123')

#一个标准的get方法，使用？传递参数
@app.route('/api/v1.0/testget',methods=['GET'])
def getemp():
    if request.args is None:
        return abort(501)
    internaldata = request.args.to_dict()
    empname = internaldata.get('empname')
    return jsonify(empname)


@app.errorhandler(404)
def pagenotfound(error):
    return make_response(jsonify({'error':'PAGE NOT FOUND!'}),404)
@app.errorhandler(501)
def internalerror(error):
    return make_response(jsonify({'error':'INTERNAL ERROR!'}),501)
@app.errorhandler(503)
def inputargserror(error):
    return make_response(jsonify({'error':'INPUT PARAMETER ERROR!'}),503)
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
