``

## 更新说明
V1.0

## 配置说明

+ 配置数据库
数据库默认使用sqlite，也可以使用postgres container，cd到postgres目录下，pull镜像，启动。
数据库URI地址由数据库名、用户名、密码、主机、端口号组成。
```
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/wr_prd'
```
步骤见postgres目录下的readme.md

+  配置config.py

`DEPARTMENTS`: 这个元组为部门列表，第一次打开时自动初始化到数据库中，用户在注册时可以选择部门。

`MAIL_USERNAME` : 用来发送邮件通知的邮箱账号

`MAIL_PASSWORD` : 用来发送邮件通知的邮箱密码


## 后台管理

第一次注册的用户为超级管理员，永远有登录后台的权限。
管理员可以修改其他角色

默认用户角色为`EMPLOYEE`，仅具有读写自己的周报的权限，

`MANAGER`可以读写周报，并查看本部门所有周报。而HR可以读写周报，并查看全部门所有周报。

`ADMINISTRATOR`在HR基础上增加了进入后台的功能。

`QUIT`用来标识离职后的员工，禁止其登录。
