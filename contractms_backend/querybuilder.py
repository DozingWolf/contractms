import os
from enum import Enum,unique

@unique
class queryType(Enum):
    nonetype = 0
    select = 1
    insert = 2
    update = 3

class queryTypeError(Exception):
    def __init__(self,msg):
        self.msg = msg
    
    def __str__(self):
        return str(self.msg)

    def __repr__(self):
        return 'queryTypeError , input type is:'+type(self.msg)+', input value is:'+self.msg

class queryConditionError(Exception):
    def __init__(self,msg):
        self.msg = msg
    
    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'queryConditionError :'

class noLogHandlerError(Exception):
    def __init__(self,msg):
        self.msg = msg
    
    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'noLogHandlerError :'

class whereConditionError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'whereConditionError :'

class updataConditionError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'updateConditionError :'
class tableNameError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'tableNameError :'

class queryBuilderFactory(object):
    # 这个查询语句构造工具暂时仅适配oracle数据库
    # 原因为虽然全部使用标准TSQL，且遵循良好sql要求，但无法保证在所有支持TSQL的平台上能够得到良好执行效率
    # oracle的自我优化能力较好，执行效率较好
    # SQL server可以有限尝试，不保证sql执行效率
    # MySQL需要对sql文进行优化，不建议尝试
    # pg未实验，如有人有兴趣可以自行测试
    # 本构造工具需要与cx_Oracle等数据库连接工具配合使用
    # 暂时不支持输出原生sql，因where条件内的绑定字符参数和普通字符串会混淆，难以判断
    def __init__(self,tname = '',loghandler = None,debugmode = 1):
        # 判断是否为调试模式，未来希望控制输出日志的等级
        if debugmode == 0:
            if loghandler == None:
                print('class [queryBuilderFactory] need a loghandler to initial')
                raise noLogHandlerError('class [queryBuilderFactory] need a loghandler to initial')
        elif debugmode == 1:
            pass
        if tname:
            if type(tname) == list:
                pass
            elif type(tname) == str:
                self.__tableName = tname
            else:
                raise tableNameError('class [queryBuilderFactory] initial arg[tname] type must in(str,list)') 
        else:
            raise tableNameError('class [queryBuilderFactory] need import arg: [tname]')
        
        self.__baseQuerySelect = 'select'
        self.__baseQueryUpdate = 'update'
        self.__baseQueryInsert = 'insert into'
    
    def getTableName(self):
        return self.__tableName

    def queryBuilder(self,qtype:enumerate,**querycondition):  
    # 查询构建器的设计思路：传入sql语句类型，提供select、update、insert三种方式
    # **querycondition可变参数传入查询条件和赋值条件，需要以dict的形式传入一个{key:value}键值对
    # 逐一查询条件逐步构建，构建完成的查询条件部分append进self.__querySet过程变量内，这个变量是个list
    # 待全部完成后，利用' '.join(self.__querySet)函数进行查询条件的加空格拼接
    # **querycondition字典的结构为:
    # {'where':{key1:value1,key2:value2...},'update':{key1:value1,key2:value2,...},
    # 'insert':{[col1_key1:value1,col1_key2:value2,...],[col_key1:value1,col2_key2:value2,...],[...]...}
    # 'resultcolname':['col1','col2','col3',...]}
    # 标准的sql模板：
    # 单表
    # select : select col1,col2,col3,... from Ta where col_n = something and col_n+1 = something and...
    # update : update Ta set col1 = something ,col2 = something ,... where col_n = something and col_n+1 = something and...
    # insert : 
    # 多表
    # select : ...
        self.__querySet = []
        if qtype is queryType.select:
            # 先判断必须的where、resultcolname值是否有传输和为空
            if 'where' not in querycondition:
                raise whereConditionError('input args [**querycondition] havn\'t key:where')
            if 'resultcolname' not in querycondition:
                raise whereConditionError('input args [**querycondition] havn\'t key:resultcolname')
            if not querycondition.get('resultcolname'):
                raise whereConditionError('input args [**querycondition] need key [resultcolname] not null')
            # 开始构造基本的sql内容
            self.__querySet.append(self.__baseQuerySelect)
            # resultcolname是一个list，用逗号隔开拼接
            self.__querySet.append(', '.join(querycondition.get('resultcolname')))
            # 添加from关键词
            self.__querySet.append('from')
            # 添加表名
            self.__querySet.append(self.__tableName)
            # 开始where条件的处理
            if not querycondition.get('where'):
                # 判断查询条件字典数据是否为空，为空直接跳过
                # 构造工具兼容无where条件的情况，如果需要控制where条件必须输入在业务代码内控制
                pass
            else:
                # 不为空情况下开始构造查询的where部分
                self.__querySet.append('where')
                self.__tempQueryWhereCondition = querycondition.get('where')
                for wherecondition in querycondition.get('where').keys():
                    self.__querySet.append(wherecondition)
                    self.__querySet.append('=')
                    self.__querySet.append(str(self.__tempQueryWhereCondition.get(wherecondition)))
                    self.__querySet.append('and')
                # 去除最后的and
                self.__querySet.pop(-1)
            print(self.__querySet)
            self.__querySql = ' '.join(self.__querySet)
            print('query sql: %s'%' '.join(self.__querySet))
            return self.__querySql
        elif qtype is queryType.update:
            # 先判断必须的where、update值是否有传输和为空
            # 注意，此处构造器允许全表update，不会判断是否有where条件\
            # 但是为了防止有人忘记传值造成的where条件缺失错误update，还是加上了对'where'这个key的判断
            if 'where' not in querycondition:
                raise whereConditionError('input args [**querycondition] havn\'t key:where')
            if 'update' not in querycondition:
                raise updataConditionError('input args [**querycondition] havn\'t key:update')
            if not querycondition.get('update'):
                raise updataConditionError('input args [**querycondition] need key [update] not null')
            if type(querycondition.get('update')) != dict:
                raise updataConditionError('input args [**querycondition] arg [update] not a dict')

            # 开始构造基本的sql内容
            self.__querySet.append(self.__baseQueryUpdate)
            self.__querySet.append(self.__tableName)
            self.__querySet.append('set')
            # 先拼接处理update的set部分
            self.__tempQueryUpdCondition = querycondition.get('update')
            for setcondition in querycondition.get('update').keys():
                self.__querySet.append(setcondition)
                self.__querySet.append('=')
                self.__querySet.append(str(self.__tempQueryUpdCondition.get(setcondition)))
                self.__querySet.append(',')
                # 去除最后的逗号
            self.__querySet.pop(-1)
            # 再拼接处理where条件部分
            self.__querySet.append('where')
            self.__tempQueryUpdCondition = querycondition.get('where')
            for wherecondition in querycondition.get('where').keys():
                self.__querySet.append(wherecondition)
                self.__querySet.append('=')
                self.__querySet.append(str(self.__tempQueryUpdCondition.get(wherecondition)))
                self.__querySet.append('and')
            # 去除最后的and
            self.__querySet.pop(-1)
            # list拼接空格成为输出的sql语句
            self.__querySql = ' '.join(self.__querySet)
            print('query sql: %s'%self.__querySql)
            return self.__querySql
        elif qtype is queryType.insert:
            print('querytype is %s'%qtype)
        elif qtype is queryType.nonetype:
            raise queryTypeError(qtype)
        return None
        