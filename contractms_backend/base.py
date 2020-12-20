from configparser import ConfigParser
import logging
import base64
import cx_Oracle
import os

class AppInitial(object):
    def __init__(self):
        # start logging

        logging.basicConfig(filename='./log/sys.log',
                            level=logging.DEBUG,
                            format='%(asctime)s:%(name)-12s:%(levelname)-6s-%(message)s',
                            datefmt='%Y/%m/%d-%H:%M:%S')
        self.logFormat = logging.Formatter(fmt='%(asctime)s:%(name)-12s:%(levelname)-6s-%(message)s',
                                    datefmt='%Y/%m/%d-%H:%M:%S')
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.console.setFormatter(self.logFormat)
        logging.getLogger('').addHandler(self.console)
        self.sysLog = logging.getLogger('app.py')
        # load parameter

        self.paraPath = './conf/sys.conf'
        self.para = ConfigParser()
        self.para.read(self.paraPath)
        self.sysLog.debug(self.para.sections())
        self.dbIP = self.para.get('db','ip')
        self.dbPort = self.para.get('db','port')
        self.dbServicename = self.para.get('db','servicename')
        self.dbSchema = self.para.get('db','schemaname')
        self.sysLog.debug('db info is [IP:%s,Port:%s,Servicename:%s,Schemaname:%s]'%(self.dbIP,self.dbPort,self.dbServicename,self.dbSchema))

        # # base64 encode

        # pwciph = base64.b64encode(para.get('db','password').encode('utf-8'))
        # self.sysLog.debug(pwciph.decode('utf-8'))
        # pw = base64.b64decode(pwciph.decode('utf-8'))
        # self.sysLog.debug(pw.decode('utf-8'))

        # base64 decode

        self.dbPassword = base64.b64decode(self.para.get('db','password')).decode('utf-8')
        self.sysLog.debug('final db password is : %s'%self.dbPassword)

        # use cxoracle to link oracle server

        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
        # db connect type tns
        try:
            self.dbTNS = cx_Oracle.makedsn(self.dbIP,self.dbPort,self.dbServicename)
            self.dbConnect = cx_Oracle.connect(self.dbSchema,self.dbPassword,self.dbTNS)
            self.sysLog.info('type 1 connected to db server')
        except Exception as err:
            self.sysLog.error('type 1 have an error:%s'%err)
    
    def getMainFunc(self):
        return self.dbConnect,self.sysLog
    
    def transCustomList2Dict(self,inputlist=[],colnamemodel=[]):
        # 用于处理数据库反馈list转换成可被前端读取的dict，供后续转json使用
        fbkMessage = {'status':'','statinfo':'','dataload':{}}
        if inputlist == []:
            fbkMessage.update({'status':'0','statinfo':'没有传入的参数inputlist'})
            return fbkMessage
        if colnamemodel == []:
            fbkMessage.update({'status':'0','statinfo':'没有传入的参数colnamemodel'})
            return fbkMessage
        if len(inputlist[0]) != len(colnamemodel):
            statinfo = '传入的数据栏目数%d个和给定的dict模板栏目数%d个不匹配，请检查参数'%(len(inputlist[0]),len(colnamemodel))
            fbkMessage.update({'status':'0','statinfo':statinfo})
            return fbkMessage
        else:
            rowcount = len(inputlist)
            columncount = len(inputlist[0])
            self.sysLog.debug('data result set has %d row(s) %d columns,'%(rowcount,columncount))
            # dataload = {'rowcount':rowcount,'dataload':{}}
            innerdatalist = []
            innerrowlist = []
            datadict = {}
            for rowno,datarow in enumerate(inputlist):
                self.sysLog.debug('row no = %d,data row = %s'%(rowno,datarow))
                # 组合列标题和数据值，并转换成dict供后续处理
                tempdataload = dict(zip(colnamemodel,datarow))
                self.sysLog.debug('tempdataload is :%s'%tempdataload)
                innerrowlist.append(rowno)
                innerdatalist.append(tempdataload)
                # for datano,datacol in enumerate(inputlist[rowno]):
                #     self.sysLog.debug('No.%d ==> %s,colname = %s'%(datano,datacol,colnamemodel[datano]))
            datadict.update(dict(zip(innerrowlist,innerdatalist)))
            self.sysLog.debug('inner datalist is %s'%innerdatalist)
            fbkMessage.update({'dataload':datadict})
            fbkMessage.update({'status':'1','statinfo':'转换成功!!'})

            return fbkMessage
