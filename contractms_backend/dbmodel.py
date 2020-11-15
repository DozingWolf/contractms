__author__ = 'DozingWolf'
import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, MetaData,Sequence
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.dialects.oracle import DATE, VARCHAR2, NUMBER
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config

def createEngine(user, password, ip, port, sid):
    db_engine = create_engine('oracle://%s:%s@%s:%d/%s' %
                              (user, password, ip, port, sid), echo=False)
    return db_engine


Base = declarative_base()
#table model
class UserModel(Base):
    __tablename__ = 'IT_MST_EMP_V'
    EMPID = Column(NUMBER,primary_key=True)
    EMPCODE = Column(VARCHAR2(20))
    EMPNAME = Column(VARCHAR2(100))
    PASSWORD = Column(VARCHAR2())
    def __repr__(self):
        return '<IT_MST_EMP_V(EMPID=%d,EMPCPDE=%s,EMPNAME=%s)>'%(self.EMPID,self.EMPCODE,self.EMPNAME)
    #readonly password
    @property
    def password_row(self):
        raise AttributeError('Read Password Error')
    #check password
    def check_password(self,password):
        return check_password_hash(self.PASSWORD,password)
    @staticmethod
    def create_token(empid):
        s = Serializer(secret_key = 'EDMOND',expires_in=3600) #未来此处改为使用config
        token = s.dump({"EMPID":empid}).decode('ascii')
        return token


class IT_CONTRACT_DTL(Base):
    __tablename__ = 'IT_CONTRACT_DTL'
    CONTRACTID = Column(NUMBER,Sequence('SEQ_IT_CONTRACT_DTL_ID'),primary_key=True,nullable=False)
    CONTRACTDTLID = Column(NUMBER)
    PRC = Column(NUMBER(10,2))
    PRICE = Column(NUMBER(10,6))
    TAX =  Column(NUMBER)
    PROVISION = Column(VARCHAR2(200))
    DTLMEMO = Column(VARCHAR2(500))
    CREATEUSER = Column(NUMBER)
    CREATEDEPT = Column(NUMBER)
    CREATEDATE = Column(DATE, default = datetime.utcnow)
    EDITUSER = Column(NUMBER)
    EDITDATE = Column(DATE)
    EDITFLAG = Column(VARCHAR2(2), default = '00')
    STOPFLAG = Column(VARCHAR2(2), default = '00')
    MERGEFLAG = Column(VARCHAR2(2), default = '00')

class IT_C2P_REF(Base):
    __tablename__ = 'IT_C2P_REF'
    ID = Column(NUMBER, primary_key=True, nullable=False)
    CONTRACTDTLID = Column(NUMBER)
    LISTID = Column(NUMBER)
    CREATERUSER = Column(NUMBER)
    CREATEDEPT = Column(NUMBER)
    CREATEDATE = Column(DATE, default=datetime.utcnow)
    EDITUSER = Column(NUMBER)
    EDITDATE = Column(DATE)
    EDITFLAG = Column(VARCHAR2(2),default='00')
    STOPFLAG = Column(VARCHAR2(2),default='00')
    OWNERID = Column(NUMBER)

    def __repr__(self):
        return '<IT_C2P_REF(ID=%d,CONTRACTDTLID=%d,OWNERID=%d,LISTID=%s)>' % (self.ID, self.CONTRACTDTLID, self.OWNERID, self.LISTID)


# engine = createEngine(db_ip,db_password,db_sid,db_user,db_password)

def CreateorReplaceTable(db_engine):
    Base.metadata.create_all(db_engine)


def CreateSession(db_engine):
    session = sessionmaker(bind=db_engine)
    return session()
