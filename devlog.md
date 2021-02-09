# 开发日志
|时间|工作|
|:--|:--|
|2020-11-10|创建项目|
|2020-11-11|部署环境|
|2020-11-13|创建demo，测试get方法|
|2020-12-13|数据库连接demo，添加config读取器和log记录器，数据库连接使用cxOracle完成。ORM方面考虑python代码实现复杂度和开发者对sql的熟悉程度，暂时不考虑使用sqlAlchemy了。先利用cxOracle来执行sql获取反馈|
|2020-12-25|前几天尝试写一个登录的token实现，尝试可以下发现好像暂时对flask的理解还是比较薄弱。暂时先不折腾token，优先精力实现CURD业务功能|
|2021-01-01|写了一个简易的SQL构造器，先实现查询select和更新update，准备实现单行insert和批量insert。|
|2020-01-02|开发者考虑再查询构建器内加一个表字段名和数据类型获取器，给类里面传入一个dbhandler试试看|
|2021-01-04|dbhandler成功，尝试再__init__内动态setattr，成功|
|2021-01-05|利用链式调用设计sql构造思路，调用链路：sql,paradata = table('Ta').select(table.colA,table.colB,table.colC,...).where(contain(table.colA,[10,20,5,56,...])).and(eq(table.colB,'90')).or(eq(table.colC,33)).....get(returntype = str[/list]) 使对象调用方法尽量符合传统sql的书写方式，便于使用|
|2021-01-16|链式调用已经实现了，现在希望能够返回一组可以直接使用的查询报文和查询参数dict，同时查询参数可以自增变量编号|