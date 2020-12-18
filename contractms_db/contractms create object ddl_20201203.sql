prompt PL/SQL Developer Export User Objects for user CONTRACTMS@CMSGRYL
prompt Created by GKRD_IT_03_NEW on 2020��12��17��
set define off
spool contractms create object ddl_20201203.log

prompt
prompt Creating table IT_C2P_REF
prompt =========================
prompt
create table CONTRACTMS.IT_C2P_REF
(
  id            NUMBER not null,
  contractdtlid NUMBER,
  listid        NUMBER,
  createuser    NUMBER,
  createdept    NUMBER,
  createdate    DATE default sysdate,
  edituser      NUMBER,
  editdate      DATE,
  editflag      VARCHAR2(2) default '00',
  stopflag      VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on table CONTRACTMS.IT_C2P_REF
  is '��ͬ��ϸ�ո�����ϸ������';
comment on column CONTRACTMS.IT_C2P_REF.id
  is '��������';
comment on column CONTRACTMS.IT_C2P_REF.contractdtlid
  is '��ͬ��ϸid';
comment on column CONTRACTMS.IT_C2P_REF.listid
  is '�ո����嵥id';
comment on column CONTRACTMS.IT_C2P_REF.createuser
  is '����������';
comment on column CONTRACTMS.IT_C2P_REF.createdept
  is '������������';
comment on column CONTRACTMS.IT_C2P_REF.createdate
  is '��������ʱ��';
comment on column CONTRACTMS.IT_C2P_REF.edituser
  is '�޸���';
comment on column CONTRACTMS.IT_C2P_REF.editdate
  is '�޸�ʱ��';
comment on column CONTRACTMS.IT_C2P_REF.editflag
  is '�޸ı��,00δ�޸ģ�10���޸�';
comment on column CONTRACTMS.IT_C2P_REF.stopflag
  is '���ñ��,00������10�ѽ���';
create index CONTRACTMS.IT_C2P_REF_CONTRACTDTLID on CONTRACTMS.IT_C2P_REF (CONTRACTDTLID)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
create index CONTRACTMS.IT_C2P_REF_LISTID on CONTRACTMS.IT_C2P_REF (LISTID)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
alter table CONTRACTMS.IT_C2P_REF
  add constraint IT_C2P_REF_ID primary key (ID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

prompt
prompt Creating table IT_CONTRACT_DTL
prompt ==============================
prompt
create table CONTRACTMS.IT_CONTRACT_DTL
(
  contractid    NUMBER,
  contractdtlid NUMBER not null,
  prc           NUMBER(10,2),
  price         NUMBER(10,6),
  tax           NUMBER,
  provision     VARCHAR2(200),
  dtlmemo       VARCHAR2(500),
  createuser    NUMBER,
  createdept    NUMBER,
  createdate    DATE default sysdate,
  edituser      NUMBER,
  editdate      DATE,
  editflag      VARCHAR2(2) default '00',
  stopflag      VARCHAR2(2) default '00',
  mergeflag     VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on table CONTRACTMS.IT_CONTRACT_DTL
  is '��Ŀ��ͬ������ϸ��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.contractid
  is '��ͬid';
comment on column CONTRACTMS.IT_CONTRACT_DTL.contractdtlid
  is '��ϸid';
comment on column CONTRACTMS.IT_CONTRACT_DTL.prc
  is '��ϸ��˰���';
comment on column CONTRACTMS.IT_CONTRACT_DTL.price
  is '��ϸ��˰���';
comment on column CONTRACTMS.IT_CONTRACT_DTL.tax
  is '��ϸ˰��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.provision
  is '��ϸ���ս�������';
comment on column CONTRACTMS.IT_CONTRACT_DTL.dtlmemo
  is '��ϸ˵��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createuser
  is '��ϸ������';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createdept
  is '��ϸ��������';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createdate
  is '��ϸ����ʱ��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.edituser
  is '�޸���';
comment on column CONTRACTMS.IT_CONTRACT_DTL.editdate
  is '�޸�ʱ��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.editflag
  is '�޸ı��,00����,10���޸�';
comment on column CONTRACTMS.IT_CONTRACT_DTL.stopflag
  is '���ñ��,00����,10ͣ��';
comment on column CONTRACTMS.IT_CONTRACT_DTL.mergeflag
  is '�ϲ������ǣ�00���ϲ���10�ϲ�';
create unique index CONTRACTMS.IT_CONTRACT_DTL_DTLID on CONTRACTMS.IT_CONTRACT_DTL (CONTRACTDTLID)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
create index CONTRACTMS.IT_CONTRACT_DTL_HDRID on CONTRACTMS.IT_CONTRACT_DTL (CONTRACTID)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
alter table CONTRACTMS.IT_CONTRACT_DTL
  add constraint IT_CONTRACT_DTL_ID primary key (CONTRACTDTLID);

prompt
prompt Creating table IT_CONTRACT_HDR
prompt ==============================
prompt
create table CONTRACTMS.IT_CONTRACT_HDR
(
  contractid        NUMBER not null,
  contractcode      VARCHAR2(50),
  contractname      VARCHAR2(150),
  partaid           NUMBER,
  partaname         VARCHAR2(100),
  partbid           NUMBER,
  partbname         VARCHAR2(100),
  partcid           NUMBER,
  partcname         VARCHAR2(100),
  contracttype      VARCHAR2(2) default '00',
  contractmemo      VARCHAR2(500),
  contractstartdate DATE default sysdate,
  contractenddate   DATE default sysdate+365,
  createuser        NUMBER,
  createdept        NUMBER,
  createdate        DATE default sysdate,
  executor          NUMBER,
  executdept        NUMBER,
  edituser          NUMBER,
  editdate          DATE,
  editflag          VARCHAR2(2) default '00',
  stopflag          VARCHAR2(2) default '00',
  contractprc       NUMBER(10,2),
  invtype           VARCHAR2(2) default '00',
  paytype           VARCHAR2(2) default '00',
  prjflag           NUMBER default 16
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on table CONTRACTMS.IT_CONTRACT_HDR
  is '��Ŀ��ͬ��������';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractid
  is '��ͬ����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractcode
  is '��ͬ����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractname
  is '��ͬ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partaid
  is '�׷�����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partaname
  is '�׷���';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partbid
  is '�ҷ�����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partbname
  is '�ҷ���';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partcid
  is '����������';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partcname
  is '��������';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contracttype
  is '�������۱��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractmemo
  is '��ͬ˵��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractstartdate
  is '��ͬ��ʼʱ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractenddate
  is '��ͬ����ʱ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createuser
  is '��ͬ������';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createdept
  is '��ͬ��������';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createdate
  is '��ͬ����ʱ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.executor
  is '��ִͬ����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.executdept
  is '��ִͬ�в���';
comment on column CONTRACTMS.IT_CONTRACT_HDR.edituser
  is '�޸���';
comment on column CONTRACTMS.IT_CONTRACT_HDR.editdate
  is '�޸�ʱ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.editflag
  is '�޸ı�ǣ�00������10���޸�';
comment on column CONTRACTMS.IT_CONTRACT_HDR.stopflag
  is '���ñ�ǣ�00������10����';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractprc
  is '��ͬ��˰�ܽ��';
comment on column CONTRACTMS.IT_CONTRACT_HDR.invtype
  is '��Ʊ����''00''��ֵ˰ר�ã�''10''��ֵ˰��ͨ';
comment on column CONTRACTMS.IT_CONTRACT_HDR.paytype
  is '���ʽ';
comment on column CONTRACTMS.IT_CONTRACT_HDR.prjflag
  is '��Ŀ���ͣ��μ�parameter type=PARA002��Ĭ��16����Ŀ';
create unique index CONTRACTMS.IT_CONTRACT_HDR_HDRID on CONTRACTMS.IT_CONTRACT_HDR (CONTRACTID)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
alter table CONTRACTMS.IT_CONTRACT_HDR
  add constraint IT_CONTRACT_HDR_ID primary key (CONTRACTID);

prompt
prompt Creating table IT_MST_CLIENTS_LIST
prompt ==================================
prompt
create table CONTRACTMS.IT_MST_CLIENTS_LIST
(
  cstid      NUMBER not null,
  cstcode    VARCHAR2(10),
  cstname    VARCHAR2(150),
  taxidno    VARCHAR2(50),
  addr       VARCHAR2(200),
  tel        VARCHAR2(20),
  banklistid NUMBER,
  createuser NUMBER,
  createdept NUMBER,
  createdate DATE default sysdate,
  edituser   NUMBER,
  editdate   DATE,
  editflag   VARCHAR2(2) default '00',
  stopflag   VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.cstid
  is '����id';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.cstcode
  is '���̱���';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.cstname
  is '��������';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.taxidno
  is '��˰��ʶ���';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.addr
  is '�����ʼĵ�ַ';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.tel
  is '��ϵ�绰';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.banklistid
  is '�������й���id';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createuser
  is '������';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createdept
  is '��������';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createdate
  is '����ʱ��';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.edituser
  is '�޸���';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.editdate
  is '�޸�ʱ��';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.editflag
  is '�޸ı��';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.stopflag
  is '���ñ��';
alter table CONTRACTMS.IT_MST_CLIENTS_LIST
  add constraint IT_MST_CLIENTS_LIST_ID primary key (CSTID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

prompt
prompt Creating table IT_MST_DEPT
prompt ==========================
prompt
create table CONTRACTMS.IT_MST_DEPT
(
  deptid     NUMBER not null,
  deptcode   VARCHAR2(10),
  ownerid    NUMBER,
  deptmemo   VARCHAR2(100),
  createuser NUMBER,
  createdate DATE default sysdate,
  edituser   NUMBER,
  editdate   DATE,
  editflag   VARCHAR2(2) default '00',
  stopflag   VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on column CONTRACTMS.IT_MST_DEPT.deptid
  is '����id';
comment on column CONTRACTMS.IT_MST_DEPT.deptcode
  is '���ű���';
comment on column CONTRACTMS.IT_MST_DEPT.ownerid
  is '����';
comment on column CONTRACTMS.IT_MST_DEPT.deptmemo
  is '����˵��';
comment on column CONTRACTMS.IT_MST_DEPT.createuser
  is '������';
comment on column CONTRACTMS.IT_MST_DEPT.createdate
  is '����ʱ��';
comment on column CONTRACTMS.IT_MST_DEPT.edituser
  is '�޸���';
comment on column CONTRACTMS.IT_MST_DEPT.editdate
  is '�޸�ʱ��';
comment on column CONTRACTMS.IT_MST_DEPT.editflag
  is '�޸ı�� 00δ�޸ģ�10���޸�';
comment on column CONTRACTMS.IT_MST_DEPT.stopflag
  is '���ñ�� 00������10�ѽ���';
alter table CONTRACTMS.IT_MST_DEPT
  add constraint IT_MST_DEPT_ID primary key (DEPTID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

prompt
prompt Creating table IT_PARAMETER_LIST
prompt ================================
prompt
create table CONTRACTMS.IT_PARAMETER_LIST
(
  id         NUMBER not null,
  paratype   VARCHAR2(10),
  paraindex  VARCHAR2(30),
  paravalue  VARCHAR2(50),
  parameter  VARCHAR2(400),
  createuser NUMBER,
  createdept NUMBER,
  createdate DATE default sysdate,
  edituser   NUMBER,
  editdate   DATE,
  editflag   VARCHAR2(2) default '00',
  stopflag   VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on table CONTRACTMS.IT_PARAMETER_LIST
  is '�������ñ�';
create index CONTRACTMS.IT_PARAMETER_LIST_INDEX on CONTRACTMS.IT_PARAMETER_LIST (PARAINDEX)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
create index CONTRACTMS.IT_PARAMETER_LIST_TYPE on CONTRACTMS.IT_PARAMETER_LIST (PARATYPE)
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
alter table CONTRACTMS.IT_PARAMETER_LIST
  add constraint IT_PARAMETER_LIST_ID primary key (ID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

prompt
prompt Creating table IT_PAYORCOLLECT_LIST
prompt ===================================
prompt
create table CONTRACTMS.IT_PAYORCOLLECT_LIST
(
  listid     NUMBER not null,
  prc        NUMBER(15,2),
  price      NUMBER(15,6),
  tax        NUMBER,
  invno      VARCHAR2(13),
  invcode    VARCHAR2(10),
  invdate    DATE,
  invinfo    VARCHAR2(100),
  listtype   VARCHAR2(2) default '00',
  listmemo   VARCHAR2(500),
  invclass   NUMBER,
  createuser NUMBER,
  createdept NUMBER,
  createdate DATE default sysdate,
  edituser   NUMBER,
  editdate   DATE,
  editflag   VARCHAR2(2) default '00',
  stopflag   VARCHAR2(2) default '00'
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
comment on table CONTRACTMS.IT_PAYORCOLLECT_LIST
  is '�ո��Ʊ��';
comment on column CONTRACTMS.IT_PAYORCOLLECT_LIST.listtype
  is '00 δ��δ��״̬��10�����Ѹ�״̬';
alter table CONTRACTMS.IT_PAYORCOLLECT_LIST
  add constraint IT_PAYORCOLLECT_LIST_ID primary key (LISTID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

prompt
prompt Creating sequence IT_CONTRACT_DTL_SEQ
prompt =====================================
prompt
create sequence CONTRACTMS.IT_CONTRACT_DTL_SEQ
minvalue 1
maxvalue 999999999
start with 1
increment by 1
cache 20;

prompt
prompt Creating sequence IT_CONTRACT_HDR_SEQ
prompt =====================================
prompt
create sequence CONTRACTMS.IT_CONTRACT_HDR_SEQ
minvalue 1
maxvalue 9999999999
start with 1
increment by 1
cache 20;

prompt
prompt Creating sequence IT_PAYORCOLLECT_LIST_SEQ
prompt ==========================================
prompt
create sequence CONTRACTMS.IT_PAYORCOLLECT_LIST_SEQ
minvalue 1
maxvalue 999999999
start with 1
increment by 1
cache 20;

prompt
prompt Creating synonym IT_MST_EMP
prompt ===========================
prompt
create or replace synonym CONTRACTMS.IT_MST_EMP
  for GRYL.PUB_EMP;

prompt
prompt Creating view IT_CONTRACT_PAY_INVCLASS
prompt ======================================
prompt
create or replace force view contractms.it_contract_pay_invclass as
select
h.contractcode,h.contractname,d.provision,d.dtlmemo,
h.contractprc,d.prc as dtlprc,pl.paravalue,
sum(l.prc) as sum_inv_prc,round(sum(l.prc)/h.contractprc,2) as c2i_ratio,
decode(h.partcname,null,'N','Y') as bypassflag,/*��Ʊ��ͬ��ǣ�Y��Ʊ*/
h.partcname,pl2.paravalue as prjname
from it_contract_hdr h
inner join it_contract_dtl d on h.contractid = d.contractid and d.mergeflag = '00'
inner join it_c2p_ref r on d.contractdtlid = r.contractdtlid
inner join it_payorcollect_list l on r.listid = l.listid
inner join it_parameter_list pl on l.invclass = pl.id
inner join it_parameter_list pl2 on h.prjflag = pl2.id
where 1=1
group by h.contractcode,h.contractname,d.provision,d.dtlmemo,h.contractprc,d.prc,pl.paravalue,h.partcname,pl2.paravalue

union all

/*�ϲ�����*/
select
h.contractcode,h.contractname,d.provision,d.dtlmemo,
h.contractprc,d.prc as dtlprc,pl.paravalue,
sum(d.prc) as sum_inv_prc,round(sum(l.prc)/h.contractprc,2) as c2i_ratio,
decode(h.partcname,null,'N','Y') as bypassflag,/*��Ʊ��ͬ��ǣ�Y��Ʊ*/
h.partcname,pl2.paravalue as prjname
from it_contract_hdr h
inner join it_contract_dtl d on h.contractid = d.contractid and d.mergeflag = '10'
inner join it_c2p_ref r on d.contractdtlid = r.contractdtlid
inner join it_payorcollect_list l on r.listid = l.listid
inner join it_parameter_list pl on l.invclass = pl.id
inner join it_parameter_list pl2 on h.prjflag = pl2.id
where 1=1
group by h.contractcode,h.contractname,d.provision,d.dtlmemo,h.contractprc,d.prc,pl.paravalue,h.partcname,pl2.paravalue;

prompt
prompt Creating view IT_FIN_UNPAY_LIST
prompt ===============================
prompt
create or replace force view contractms.it_fin_unpay_list as
select
h.CONTRACTCODE, h.CONTRACTNAME, h.PARTBNAME, h.PARTCNAME,h.contractprc,
d.prc,round((d.prc/h.contractprc),2) as unpayproportion,d.provision,
h.contracttype
from
it_contract_hdr h inner join it_contract_dtl d on h.contractid = d.contractid
left join it_c2p_ref r on d.contractdtlid = r.contractdtlid
left join it_payorcollect_list l on r.listid = l.listid
where 1=1
--and l.invno is null
--and h.contracttype = '00'
and (l.listtype = '00' or nvl(l.listtype,'00') = '00')  --���������ڹ���δ������Ŀ
group by h.CONTRACTCODE, h.CONTRACTNAME, h.PARTBNAME, h.PARTCNAME,h.contractprc,d.prc,
d.provision,h.contracttype
;

prompt
prompt Creating view IT_INVCLASS_SUMVALUE
prompt ==================================
prompt
create or replace force view contractms.it_invclass_sumvalue as
select pl.PARATYPE,pl.PARAVALUE,sum(l.prc) as sumvalue from it_payorcollect_list l
inner join it_parameter_list pl on l.invclass = pl.id and pl.paratype = 'PARA001'
group by pl.PARATYPE,pl.PARAVALUE;

prompt
prompt Creating view IT_INVOICE_DTLINFO
prompt ================================
prompt
create or replace force view contractms.it_invoice_dtlinfo as
select
l.listid,l.prc,l.price,l.tax,l.invno,
l.invcode,h.contractcode,h.contractname,p2.paravalue as prjname,
p.paravalue as classname
from it_payorcollect_list l
inner join it_parameter_list p on l.invclass = p.id and p.paratype = 'PARA001'
inner join it_c2p_ref r on r.listid = l.listid
inner join it_contract_dtl d on d.contractdtlid = r.contractdtlid
inner join it_contract_hdr h on h.contractid = d.contractid
inner join it_parameter_list p2 on h.prjflag = p2.id and p2.paratype = 'PARA002'
where 1=1
and l.invno is not null
group by
l.listid,l.prc,l.price,l.tax,l.invno,l.invcode,h.contractcode,h.contractname,p2.paravalue,p.paravalue;

prompt
prompt Creating view IT_MST_EMP_V
prompt ==========================
prompt
create or replace force view contractms.it_mst_emp_v as
select EMPID, EMPCODE, EMPNAME, PASSWORD
from it_mst_emp
where stopflag = '00';


prompt Done
spool off
set define on
