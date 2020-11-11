----------------------------------------------------
-- Export file for user CONTRACTMS@CMSGRYL        --
-- Created by chenshengyu on 2020/11/11, 17:12:39 --
----------------------------------------------------

set define off
spool contractms create object ddl.log

prompt
prompt Creating table IT_C2P_REF
prompt =========================
prompt
create table CONTRACTMS.IT_C2P_REF
(
  id            NUMBER,
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
  is '合同明细收付款明细关联表';
comment on column CONTRACTMS.IT_C2P_REF.id
  is '关联主键';
comment on column CONTRACTMS.IT_C2P_REF.contractdtlid
  is '合同明细id';
comment on column CONTRACTMS.IT_C2P_REF.listid
  is '收付款清单id';
comment on column CONTRACTMS.IT_C2P_REF.createuser
  is '关联创建人';
comment on column CONTRACTMS.IT_C2P_REF.createdept
  is '关联创建部门';
comment on column CONTRACTMS.IT_C2P_REF.createdate
  is '关联创建时间';
comment on column CONTRACTMS.IT_C2P_REF.edituser
  is '修改人';
comment on column CONTRACTMS.IT_C2P_REF.editdate
  is '修改时间';
comment on column CONTRACTMS.IT_C2P_REF.editflag
  is '修改标记,00未修改，10已修改';
comment on column CONTRACTMS.IT_C2P_REF.stopflag
  is '禁用标记,00正常，10已禁用';
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
create unique index CONTRACTMS.IT_C2P_REF_ID on CONTRACTMS.IT_C2P_REF (ID)
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

prompt
prompt Creating table IT_CONTRACT_DTL
prompt ==============================
prompt
create table CONTRACTMS.IT_CONTRACT_DTL
(
  contractid    NUMBER,
  contractdtlid NUMBER,
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
  is '项目合同管理明细表';
comment on column CONTRACTMS.IT_CONTRACT_DTL.contractid
  is '合同id';
comment on column CONTRACTMS.IT_CONTRACT_DTL.contractdtlid
  is '明细id';
comment on column CONTRACTMS.IT_CONTRACT_DTL.prc
  is '明细含税金额';
comment on column CONTRACTMS.IT_CONTRACT_DTL.price
  is '明细无税金额';
comment on column CONTRACTMS.IT_CONTRACT_DTL.tax
  is '明细税率';
comment on column CONTRACTMS.IT_CONTRACT_DTL.provision
  is '明细验收交付条款';
comment on column CONTRACTMS.IT_CONTRACT_DTL.dtlmemo
  is '明细说明';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createuser
  is '明细创建人';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createdept
  is '明细创建部门';
comment on column CONTRACTMS.IT_CONTRACT_DTL.createdate
  is '明细创建时间';
comment on column CONTRACTMS.IT_CONTRACT_DTL.edituser
  is '修改人';
comment on column CONTRACTMS.IT_CONTRACT_DTL.editdate
  is '修改时间';
comment on column CONTRACTMS.IT_CONTRACT_DTL.editflag
  is '修改标记,00正常,10已修改';
comment on column CONTRACTMS.IT_CONTRACT_DTL.stopflag
  is '禁用标记,00正常,10停用';
comment on column CONTRACTMS.IT_CONTRACT_DTL.mergeflag
  is '合并付款标记，00不合并，10合并';
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

prompt
prompt Creating table IT_CONTRACT_HDR
prompt ==============================
prompt
create table CONTRACTMS.IT_CONTRACT_HDR
(
  contractid        NUMBER,
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
  paytype           VARCHAR2(2) default '00'
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
  is '项目合同管理主表';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractid
  is '合同内码';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractcode
  is '合同编码';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractname
  is '合同名';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partaid
  is '甲方编码';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partaname
  is '甲方名';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partbid
  is '乙方编码';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partbname
  is '乙方名';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partcid
  is '关联方编码';
comment on column CONTRACTMS.IT_CONTRACT_HDR.partcname
  is '关联方名';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contracttype
  is '购买销售标记';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractmemo
  is '合同说明';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractstartdate
  is '合同开始时间';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractenddate
  is '合同结束时间';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createuser
  is '合同创建人';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createdept
  is '合同创建部门';
comment on column CONTRACTMS.IT_CONTRACT_HDR.createdate
  is '合同创建时间';
comment on column CONTRACTMS.IT_CONTRACT_HDR.executor
  is '合同执行人';
comment on column CONTRACTMS.IT_CONTRACT_HDR.executdept
  is '合同执行部门';
comment on column CONTRACTMS.IT_CONTRACT_HDR.edituser
  is '修改人';
comment on column CONTRACTMS.IT_CONTRACT_HDR.editdate
  is '修改时间';
comment on column CONTRACTMS.IT_CONTRACT_HDR.editflag
  is '修改标记，00正常，10已修改';
comment on column CONTRACTMS.IT_CONTRACT_HDR.stopflag
  is '禁用标记，00正常，10禁用';
comment on column CONTRACTMS.IT_CONTRACT_HDR.contractprc
  is '合同含税总金额';
comment on column CONTRACTMS.IT_CONTRACT_HDR.invtype
  is '发票类型''00''增值税专用，''10''增值税普通';
comment on column CONTRACTMS.IT_CONTRACT_HDR.paytype
  is '付款方式';
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

prompt
prompt Creating table IT_MST_CLIENTS_LIST
prompt ==================================
prompt
create table CONTRACTMS.IT_MST_CLIENTS_LIST
(
  cstid      NUMBER,
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
  is '客商id';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.cstcode
  is '客商编码';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.cstname
  is '客商名称';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.taxidno
  is '纳税人识别号';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.addr
  is '客商邮寄地址';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.tel
  is '联系电话';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.banklistid
  is '开户银行关联id';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createuser
  is '创建人';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createdept
  is '创建部门';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.createdate
  is '创建时间';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.edituser
  is '修改人';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.editdate
  is '修改时间';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.editflag
  is '修改标记';
comment on column CONTRACTMS.IT_MST_CLIENTS_LIST.stopflag
  is '禁用标记';

prompt
prompt Creating table IT_MST_DEPT
prompt ==========================
prompt
create table CONTRACTMS.IT_MST_DEPT
(
  deptid     NUMBER,
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
  is '部门id';
comment on column CONTRACTMS.IT_MST_DEPT.deptcode
  is '部门编码';
comment on column CONTRACTMS.IT_MST_DEPT.ownerid
  is '货主';
comment on column CONTRACTMS.IT_MST_DEPT.deptmemo
  is '部门说明';
comment on column CONTRACTMS.IT_MST_DEPT.createuser
  is '创建人';
comment on column CONTRACTMS.IT_MST_DEPT.createdate
  is '创建时间';
comment on column CONTRACTMS.IT_MST_DEPT.edituser
  is '修改人';
comment on column CONTRACTMS.IT_MST_DEPT.editdate
  is '修改时间';
comment on column CONTRACTMS.IT_MST_DEPT.editflag
  is '修改标记 00未修改，10已修改';
comment on column CONTRACTMS.IT_MST_DEPT.stopflag
  is '禁用标记 00正常，10已禁用';

prompt
prompt Creating table IT_PARAMETER_LIST
prompt ================================
prompt
create table CONTRACTMS.IT_PARAMETER_LIST
(
  id         NUMBER,
  paratype   VARCHAR2(10),
  paraindex  VARCHAR2(30),
  paravalue  VARCHAR2(50),
  parameter  VARCHAR2(300),
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
  is '参数配置表';
create unique index CONTRACTMS.IT_PARAMETER_LIST_ID on CONTRACTMS.IT_PARAMETER_LIST (ID)
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

prompt
prompt Creating table IT_PAYORCOLLECT_LIST
prompt ===================================
prompt
create table CONTRACTMS.IT_PAYORCOLLECT_LIST
(
  listid     NUMBER,
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
  is '收付款发票表';
create unique index CONTRACTMS.IT_PAYORCOLLECT_LIST_ID on CONTRACTMS.IT_PAYORCOLLECT_LIST (LISTID)
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
decode(h.partcname,null,'N','Y') as bypassflag,/*过票合同标记，Y过票*/
h.partcname
from it_contract_hdr h
inner join it_contract_dtl d on h.contractid = d.contractid and d.mergeflag = '00'
inner join it_c2p_ref r on d.contractdtlid = r.contractdtlid
inner join it_payorcollect_list l on r.listid = l.listid
inner join it_parameter_list pl on l.invclass = pl.id
where 1=1
group by h.contractcode,h.contractname,d.provision,d.dtlmemo,h.contractprc,d.prc,pl.paravalue,h.partcname

union all

/*合并付款*/
select
h.contractcode,h.contractname,d.provision,d.dtlmemo,
h.contractprc,d.prc as dtlprc,pl.paravalue,
sum(d.prc) as sum_inv_prc,round(sum(l.prc)/h.contractprc,2) as c2i_ratio,
decode(h.partcname,null,'N','Y') as bypassflag,/*过票合同标记，Y过票*/
h.partcname
from it_contract_hdr h
inner join it_contract_dtl d on h.contractid = d.contractid and d.mergeflag = '10'
inner join it_c2p_ref r on d.contractdtlid = r.contractdtlid
inner join it_payorcollect_list l on r.listid = l.listid
inner join it_parameter_list pl on l.invclass = pl.id
where 1=1
group by h.contractcode,h.contractname,d.provision,d.dtlmemo,h.contractprc,d.prc,pl.paravalue,h.partcname;

prompt
prompt Creating view IT_INVCLASS_SUMVALUE
prompt ==================================
prompt
create or replace force view contractms.it_invclass_sumvalue as
select pl.PARATYPE,pl.PARAVALUE,sum(l.prc) as sumvalue from it_payorcollect_list l
inner join it_parameter_list pl on l.invclass = pl.id and pl.paratype = 'PARA001'
group by pl.PARATYPE,pl.PARAVALUE;

prompt
prompt Creating view IT_MST_EMP_V
prompt ==========================
prompt
create or replace force view contractms.it_mst_emp_v as
select EMPID, EMPCODE, EMPNAME, PASSWORD
from it_mst_emp
where stopflag = '00';


spool off
