import os
from enum import Enum,unique

@unique
class queryType(Enum):
    nonetype = 0
    select = 1
    insert = 2
    update = 3

@unique
class returnType(Enum):
    strSql = 0
    listSql = 1

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
class getSqlError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
    
    def __repr__(self):
        return 'getSqlError :'

class queryBuilderFactory(object):
    # 这个查询语句构造工具暂时仅适配oracle数据库
    # 原因为虽然全部使用标准TSQL，且遵循良好sql要求，但无法保证在所有支持TSQL的平台上能够得到良好执行效率
    # oracle的自我优化能力较好，执行效率较好
    # SQL server可以有限尝试，不保证sql执行效率
    # MySQL需要对sql文进行优化，不建议尝试
    # pg未实验，如有人有兴趣可以自行测试
    # 本构造工具需要与cx_Oracle等数据库连接工具配合使用
    # 暂时不支持输出原生sql，因where条件内的绑定字符参数和普通字符串会混淆，难以判断
    def __init__(self,tname = '',loghandler = None,dbhandler = None,debugmode = 1):
        if tname:
            if type(tname) == list:
                pass
            elif type(tname) == str:
                self.__tableName = tname
            else:
                raise tableNameError('class [queryBuilderFactory] initial arg[tname] type must in(str,list)') 
        else:
            raise tableNameError('class [queryBuilderFactory] need import arg: [tname]')
        # 判断是否为调试模式，未来希望控制输出日志的等级
        # 0为正常模式，1为debug模式
        if debugmode == 0:
            if loghandler == None:
                print('class [queryBuilderFactory] need a loghandler to initial')
                raise noLogHandlerError('class [queryBuilderFactory] need a loghandler to initial')
        elif debugmode == 1:
            # 如果传入了db连接，用db连接进入数据库取表字段
            # 暂时为测试功能
            if not dbhandler:
                pass
            else:
                self.__dbcurs = dbhandler
                self.__colName = self.__getTableColumnsName()
                print(self.__colName)
                self.__tableColumnsNameDcit = {}
                for self.__nameInDataResult in self.__colName:
                    self.__tableColumnsNameDcit.update({self.__nameInDataResult[0]:{'columntype':self.__nameInDataResult[1],'columncomm':self.__nameInDataResult[2]}})
                    # 尝试动态注册类变量到类内
                    setattr(self,self.__nameInDataResult[0],{'columnname':self.__nameInDataResult[0],'columntype':self.__nameInDataResult[1],'columncomm':self.__nameInDataResult[2]})
                # print(self.__tableColumnsNameDcit)

        self.__baseQuerySelect = 'select'
        self.__baseQueryUpdate = 'update'
        self.__baseQueryInsert = 'insert into'
        self.__returnQuerySet = []
        self.__returnQueryConditionSet = {}
    
    def getTableName(self):
        return self.__tableName
    
    def __getTableColumnsName(self):
        # 暂时作为内部方法，不提供外部调用避免出现问题
        # 从oracle的用户视图取出相关表的字段和说明
        self.__select_table_columns_name_sql = '''
        SELECT
        COLU.COLUMN_NAME,COLU.DATA_TYPE,
        COMM.COMMENTS
        FROM USER_ALL_TABLES TAB
        INNER JOIN USER_TAB_COLUMNS COLU ON TAB.TABLE_NAME = COLU.TABLE_NAME
        INNER JOIN USER_COL_COMMENTS COMM ON COLU.TABLE_NAME = COMM.TABLE_NAME AND COLU.COLUMN_NAME = COMM.COLUMN_NAME
        WHERE TAB.TABLE_NAME = upper(:tablename)
        '''
        self.__select_table_columns_name_query_set = {'tablename':self.__tableName}
        try:
            self.__dbcurs.execute(self.__select_table_columns_name_sql,self.__select_table_columns_name_query_set)
            self.__tableColumns = self.__dbcurs.fetchall()
        except Exception as err:
            print('get table columns name error: %s'%err)
        
        # if self.__tableColumns :
        #     pass
        return self.__tableColumns

    def getColumnNameDict(self):
        # 用户外部用户获取该表字段相关信息
        if self.__tableColumnsNameDcit:
            return self.__tableColumnsNameDcit
        else:
            return None
    
    def getColumnDetail(self,colname):
        # 用于获取处理得到的字段具体信息
        if colname:
            return self.__tableColumnsNameDcit.get(colname)
        else:
            return None
        

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
        
    # 上面实现了一个简单的查询构造，下面尝试使用类似orm的对象操作方式来进行实现
    def queryConditionContains(self,querycondition,querydata:list ):
        self.__select_sql_list = []
        self.__select_sql_list.append(self.__baseQuerySelect)
        self.__select_sql_list.append(self.__tableName)
        self.__select_sql_list.append('where')
        self.__select_sql_list.append(querycondition.get('columnname'))
        self.__select_sql_list.append('in (')
        self.__select_sql_list.append(','.join(map(str,querydata)))
        self.__select_sql_list.append(')')
        return ' '.join(self.__select_sql_list)
        
        # print(list(dict(querycondition=querycondition).keys())[0])
    # 尝试用python对象来处理select、update、insert事务
    # 设计函数调用方式：
    # tableA = queryBuilderFactory(tname = 'Ta',dbhandler = DBHandler)
    # tableA.selectSingleTable(tableA.ID,tableA.USERCODE).whereCondition(tableA.ID,3)[.andCondition(something,someone)].get(returntype = strSql)
    # 子过程内部利用函数来处理构造sql
    def selectTable(self,*colcondition):
        # 希望得到的结果是['select','colA,colB,colC,...','from','TableA']
        self.__colName = []
        self.__returnQuerySet.append(self.__baseQuerySelect)
        for col in colcondition:
            self.__colName.append(col.get('columnname'))
        self.__returnQuerySet.append(','.join(self.__colName))
        self.__returnQuerySet.append('from')
        self.__returnQuerySet.append(self.__tableName)
        print(self.__returnQuerySet)
        return self

    def insertTable(self,**colcondition):
        return self

    def updateTable(self,**colcondition):
        return self
    
    def setCondition(self):
        return self
    
    def whereCondition(self,inarg:tuple):#condition:list,calcset:dict):
        # where条件处理时先把前面的查询list拼合成str，并压入list
        # 入参condition必须时list，在方法内使用extend方法拼接两个list
        self.__returnQuerySet = [' '.join(self.__returnQuerySet)]
        self.__returnQuerySet.append('where')
        self.__returnQuerySet.extend(inarg[0])
        self.__returnQueryConditionSet.update(inarg[1])
        return self

    def valuesCondition(self):
        return self

    def andConnection(self,condition:list):
        self.__returnQuerySet.append('and')
        self.__returnQuerySet.extend(condition)
        return self

    def orConection(self,condition:list):
        self.__returnQuerySet.append('or')
        self.__returnQuerySet.extend(condition)
        return self
    
    def eqCalculator(self,colname,value):
        self.__returnCalcSet = []
        self.__returnCalcSet.append(colname.get('columnname'))
        self.__returnCalcSet.append('=')
        self.__returnCalcSet.append(value)
        self.__returnQueryConditionSet.update({colname.get('columnname'):value})
        print('eq calc is :',self.__returnCalcSet)
        print('eq calc set is :',self.__returnQueryConditionSet)
        return self.__returnCalcSet,self.__returnQueryConditionSet

    def notEqCalculator(self,colname,value):
        self.__returnCalcSet = []
        self.__returnCalcSet.append(colname.get('columnname'))
        self.__returnCalcSet.append('<>')
        self.__returnCalcSet.append(value)
        return self.__returnCalcSet

    def greaterThanCalculator(self,colname,value,geflag = False):
        self.__returnCalcSet = []
        self.__returnCalcSet.append(colname.get('columnname'))
        if not geflag:
            self.__returnCalcSet.append('>')
        else:
            self.__returnCalcSet.append('>=')
        self.__returnCalcSet.append(value)
        return self.__returnCalcSet

    def lessThanCalculator(self,colname,value,leflag = False):
        self.__returnCalcSet = []
        self.__returnCalcSet.append(colname.get('columnname'))
        if not leflag:
            self.__returnCalcSet.append('<')
        else:
            self.__returnCalcSet.append('<=')
        self.__returnCalcSet.append(value)
        return self.__returnCalcSet

    def containCalculator(self,colname,*condition):
        # in计算
        self.__returnCalcSet = []
        self.__returnCalcSet.append('and')
        self.__returnCalcSet.append(colname.get('columnname'))
        self.__returnCalcSet.append('in')
        self.__returnCalcSet.append('(')
        self.__returnCalcSet.extend(condition)
        self.__returnCalcSet.append(')')
        return self.__returnCalcSet

    def getsql(self, returntype = returnType.strSql):
        # 根据需要返回字符串类型或者list类型的sql，同时返回构造好的查询绑定变量dict
        self.__returnParaSet = self.__returnQueryConditionSet
        self.__returnQuerySet.append(';')
        if returntype == returnType.strSql:
            print('data is ',self.__returnQuerySet)
            self.__returnData = ' '.join(self.__returnQuerySet)
            self.__returnQuerySet = []
        elif returntype == returnType.listSql:
            self.__returnData = self.__returnQuerySet
            self.__returnQuerySet = []
        else:
            raise getSqlError('get return type error')
        return self.__returnData,self.__returnParaSet