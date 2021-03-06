# 合同管理系统接口设计文档
## 日志
|编号|时间|操作|内容|操作人|
|:--|:--|:--|:--|--:|
|1|2020-11-08|创建|文档创建|陈圣俞|

## 文档目录

## 接口清单
1. 合同新增（主从一并新增）
2. 合同修改（包括主从）
3. 收付款信息新增
4. 收付款信息修改
5. 基础信息新增
6. 基础信息修改
7. 基础信息查询
8. 合同简单查询（主从简单展现）
9. 收付款信息查询（收付款关联合同展现）
10. 合同汇总报表查询
11. 收付款汇总报表查询
12. 用户登陆接口

## 合同新增（主从一并新增）
### 功能说明
本接口用于创建合同。要求一次性新增合同主信息以及合同明细信息。合同明细信息最少需要一条，不可以单独创建合同主信息而不提供合同明细内容。
### 接口方法
**POST 方法**
### 接口参数说明
#### 输入参数-合同主文件
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
|1|contractName|合同名|string|整个合同的命名|not null||
|2|contractPartA|合同甲方|int|合同甲方客商ID|not null||
|3|contractPartB|合同乙方|int|合同乙方客商ID|not null||
|4|contractPartC|合同关联方|int|合同关联方客商ID|nullable||
|5|contractInitiator|合同创建人|int|合同创建人的用户ID|not null||
|6|contractIniDept|合同创建部门|int|合同创建人所属部门ID|not null||
|7|contractStartDate|合同期开始时间|string|合同定义开始时间|nullable||
|8|contractEndDate|合同期结束时间|string|合同定义结束时间，若开始时间没有定义，结束时间可视为交付时间|not null||
|9|contractType|合同类型|string|合同类型，定义采购或销售，未来存在业务可拓展|not null||
|10|contractPrc|合同总金额|float|合同总计金额，应该与合同明细金额汇总相等|not null||
#### 输入参数-合同明细文件
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
|1|contractDtlPrc|合同明细付款汗水含税金额|float|合同收付款明细金额|not null||
|2|contractDtlTaxrate|明细税率|float|明细税率，按国家税率要求进行|not null||
|3|contractDtlProuision|明细付款条件|string|记录付款条件文字说明|not null||
|4|contractDtlContent|合同明细内容|string|该付款条件所涉及的合同内容|not null||
|5|contractDtlIndex|合同明细顺序编码|int|付款明细顺序编码，按照合同约定付款顺序执行|not null||
||||||||
#### 输出参数
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
|1|status|返回状态|string|写入处理返回状态，成功或失败，未来可以继续拓展|not null||
|2|rtnmessage|返回信息|json|返回的数据信息，成功为空，失败给出具体信息|nullable||
||||||||
### 接口工作流程描述
1. 登陆系统
2. 点击新增合同，给出popup的新增界面
3. 输入合同主信息，甲方、乙方、关联方、人员部门等先行使用 **【基础信息查询】** 接口得到ID并记录在后台
4. 完成合同头后点击增加明细
5. 输入明细，明细中基础信息使用方法同主信息
6. 至少输入一条明细后，允许保存
7. 保存点击后传输根据录入信息构造的json至中间业务层进行处理
8. 业务层完成处理后反馈至前台
9. 展现反馈结果给用户
10. 完成合同新增业务流
### 接口Demo
暂无，待后续编写后提供

## 合同修改（包括主从）
### 功能说明
本接口用于处理需要合同修改的情况
### 接口方法
**POST 方法**
### 接口参数说明
#### 输入参数
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
|1|contractID|合同ID|||||

### 接口工作流程描述
1. 登陆系统
2. 通过 **【合同简单查询（主从简单展现）】** 功能获取 **一个合同** 的主信息和对应的明细信息，展现并记录对应的合同ID、明细ID
3. 用户对业务规则约定可以修改的内容进行修改
4. 系统根据用户修改内容生成key-vlue对，构造修改json回传
5. 应用层处理请求并返回结果值到前台
6. 展现反馈结果给用户
7. 完成修改合同信息流程
### 接口Demo
暂无，待后续编写后提供

## 收付款信息新增

## 收付款信息修改

## 基础信息新增

## 基础信息修改

## 基础信息查询

## 合同简单查询（主从简单展现）
### 功能说明
本接口用于查询合同内容，一次查询一个合同。主要用于合同修改时使用，也可用于建立查询单一合同的查询页面。
### 接口方法
**GET 方法**
### 接口参数说明
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
|1|contractCode|合同编码|||||

## 收付款信息查询（收付款关联合同展现）

## 合同汇总报表查询

## 收付款汇总报表查询

## 用户登陆接口
### 功能说明
本接口用于用户登陆认证，并获取session
### 接口方法
**POST 方法**
### 接口参数说明
|编号|接口参数|中文名|参数类型|参数说明|为空说明||
|:--|:--|:--|:--|:--|--|--|
||||||||