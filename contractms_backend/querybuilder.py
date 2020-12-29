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

def queryBuilder(qtype:enumerate,**kwargs):  #wherecondition:dict,setcondition:dict
    if qtype not in queryType:
        raise queryTypeError(qtype)
    else:
        print(qtype)

# queryBuild(qtype=queryType['update'])
queryBuilder(qtype=12123)
# queryBuilder(qtype=queryType.select)