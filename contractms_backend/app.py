from flask import Flask,make_response,jsonify,abort,request,json,current_app
from flask_httpauth import HTTPBasicAuth
from configparser import ConfigParser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
import logging
import base64
import cx_Oracle
import os
from urllib.parse import urlencode
import signal
import sys
from baseTools import AppInitial
from querybuilder import queryBuilderFactory

mainDB = AppInitial()
dbConn,mainLog = mainDB.getMainFunc()
dbCurs = dbConn.cursor()
tkSecKey = mainDB.getSecKey()
tkExpTime = mainDB.getExpTime()
# 创建token
def createtoken(user):
    s = Serializer(tkSecKey,expires_in=tkExpTime)
    current_token = s.dumps({'user':user})
    return current_token
# 校验token
def verifytoken(token):
    s = Serializer(tkSecKey)
    try:
        data = s.loads(token)
        mainLog.debug('verifytoken loads data is %s'%data)
    except Exception as err:
        mainLog.error(' verify token err: %s'%err)
        return None
    # 查找用户    
    user = getuser_verify(usercode=data[0][0])
    return user
# 校验token装饰器
def loginverifytoken(view_func):
    @functools.wraps(view_func)
    def verifytoken(*args,**kwargs):
        try:
            token = request.headers['z-token']
        except Exception as err:
            mainLog.error('get request header token err :%s'%err)
            return jsonify(code = 4103,msg = '缺少参数token')
        s = Serializer(tkSecKey)
        try:
            s.loads(token)
            mainLog.debug('')
        except Exception as err:
            return jsonify(code = 4101,msg = "登录已过期")

def getuser_verify(usercode):
    select_it_mst_users_base = '''
    select
    USERCODE, USERNAME, USERPW
    from it_mst_users
    where 1=1
    and stopflag = '00'
    and usercode =:usercode
    '''
    select_it_mst_users_arg_set = {'usercode':usercode}
    try:
        dbCurs.execute(select_it_mst_users_base,select_it_mst_users_arg_set)
        user = dbCurs.fetchone()
    except Exception as err:
        mainLog.debug('select user err : %s'%err)
    return user

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
    table_col_name = ['usercode','username','userpw']
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
    # 使用自己编写的函数组合数据结果集，构造数据负载
    returnMessage = mainDB.transCustomList2Dict(inputlist=dbResult,colnamemodel=table_col_name)
    local_rst_set = json.dumps(returnMessage)
    print(local_rst_set)
    return make_response(local_rst_set)


@app.route('/api/v1.0/createuser/',methods=['POST'])
def createuser():
    if request.args is None:
        return abort(501)
    query_conditions = request.args.to_dict()
    mainLog.debug('get parameter is :%s'%query_conditions)
    try:
        username = query_conditions.get('username',-1)
        usercode = query_conditions.get('usercode',-1)
        userpw = query_conditions.get('userpw',-1)
    except Exception as err:
        mainLog.error('there is a error in get parament :%s'%err)
    insert_it_mst_users = '''
    insert into it_mst_users 
    (userid,username,usercode,userpw,createuser)
    values (
        it_mst_users_seq.nextval,
        :username,
        :usercode,
        :userpw,
        :createuser
    )
    '''

    insert_it_mst_users_arg_set = {'username':'','usercode':'','userpw':'','createuser':''}
    # 新增用户，不可以缺少参数！
    if username != -1:
        insert_it_mst_users_arg_set.update({'username':username})
    else:
        return abort(501)
    
    if usercode != -1:
        insert_it_mst_users_arg_set.update({'usercode':usercode})
    else:
        return abort(501)
    
    if userpw != -1:
        insert_it_mst_users_arg_set.update({'userpw':userpw})
    else:
        return abort(501)
    
    insert_it_mst_users_arg_set.update({'createuser':3})

    try:
        dbCurs.execute(insert_it_mst_users,insert_it_mst_users_arg_set)
        dbConn.commit()
        mainLog.debug('db insert success')
    except Exception as err:
        mainLog.error('insert user failed , sql: %s, para: %s'%(insert_it_mst_users,insert_it_mst_users_arg_set))
        mainLog.error('oracle return error message :%s'%err)
    return make_response({'status':'1','statinfo':'新增用户成功!!'})

@app.route('/api/v1.0/edituser/',methods=['POST'])
def edituser():
    if request.args is None:
        return abort(501)
    query_conditions = request.args.to_dict()
    mainLog.debug('get parameter is :%s'%query_conditions)
    try:
        usercode = query_conditions.get('usercode',-1)
        new_username = query_conditions.get('new_username',-1)
        new_userpw = query_conditions.get('new_userpw',-1)
    except Exception as err:
        mainLog.error('there is a error in get parament :%s'%err)
    if usercode != -1:
        # 查询条件值
        # usercode作为更新基础必须传入
        update_it_mst_user_query_set = {'usercode':usercode}
    else:
        return abort(501)
    # update语句基础部分
    update_it_mst_user_base = '''
    update it_mst_user set 
    '''
    # update语句where查询条件部分
    update_it_mst_user_quert_part = '''
    where usercode = :usercode 
    '''
    # 更新值
    update_it_mst_user_upcol = ''
    
    # 根据post方法传入的参数进行逻辑判断
    # username和userpw若传入则进行判断并构造更新体
    if new_username != -1:
        update_it_mst_user_base = update_it_mst_user_base + 'username = :new_username '
        update_it_mst_user_query_set.update({'new_username':new_username})
    # 此处需要考虑一个问题，用户行为存在几种可能性，有可能更新用户名，也可能更新用户密码
    # 未来如果存在多个情况，如何处理？
    if new_userpw != -1:
        pass
    update_it_mst_user_sql = update_it_mst_user_base + update_it_mst_user_quert_part
    mainLog.debug('update sql: %s,sql args: %s'%(update_it_mst_user_sql,update_it_mst_user_query_set))

    return make_response(update_it_mst_user_sql)



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

# 控制flask关闭时关闭数据库连接
def signal_handler(sig,act):
    mainLog.warning('system will be shutdowm...')
    mainLog.warning('close db cursor...')
    dbCurs.close()
    mainLog.warning('close db connect...')
    dbConn.close()
    mainLog.warning('db connect was closed,system has been shutdown')
signal.signal(signal.SIGINT,signal_handler)
signal.signal(signal.SIGTERM,signal_handler)

if __name__ == '__main__':
    app.run(debug=True)
