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

