__author__ = 'DozingWolf'
import json
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.dialects.oracle import DATE, VARCHAR2, NUMBER


def createEngine(user, password, ip, port, sid):
    db_engine = create_engine('oracle://%s:%s@%s:%d/%s' %
                              (user, password, ip, port, sid), echo=False)
    return db_engine


Base = declarative_base()
#table model


class ALM_WECHAT_LIST(Base):
    __tablename__ = 'ALM_WECHAT_LIST'
    ID = Column(NUMBER, primary_key=True, nullable=False)
    COMPID = Column(NUMBER)
    OWNERID = Column(NUMBER)
    BUSTYPE = Column(VARCHAR2(5))
    GENERATETIME = Column(DATE)
    MESSAGE = Column(VARCHAR2(4000))
    TRANSFLAG = Column(VARCHAR2(2))
    USERCD = Column(VARCHAR2(20))
    USERGRP = Column(VARCHAR2(10))
    USERNAME = Column(VARCHAR2(20))

    def __repr__(self):
        return '<ALM_WECHAT_LIST(ID=%d,COMPID=%d,OWNERID=%d,BUSTYPE=%s,GENERATETIME=%s,MESSAGE=%s,TRANSFLAG=%s,USERCD=%s,USERGRP=%s,USERNAME=%s)>' % (self.ID, self.COMPID, self.OWNERID, self.BUSTYPE, str(self.GENERATETIME), self.MESSAGE, self.TRANSFLAG, self.USERCD, self.USERGRP, self.USERNAME)


# engine = createEngine(db_ip,db_password,db_sid,db_user,db_password)

def CreateorReplaceTable(db_engine):
    Base.metadata.create_all(db_engine)


def CreateSession(db_engine):
    session = sessionmaker(bind=db_engine)
    return session()
