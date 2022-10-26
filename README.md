# ENV
- Python 3.9.1
- django 4.0.1
- PyCharm 2021.3.1

# Running
```bash
# project
$ cd recruitment

# install
$ pip3 install -r requirements.txt

# running
$ python manage.py runserver 0.0.0.0:8000
```

# 指定环境配置文件
```bash
$ python manage.py runserver 0.0.0.0:8000 --settings=settings.local
```

# 登录信息
> user:admin  
> password:123456

# 支持 LDAP 账号登录
[OpenLDAP 安装配置](docs/openldap.md)

# 支持钉钉发送通知
[钉钉安装配置](docs/dingtalk.md)

# 支持多语言
[多语言配置](docs/multi_language.md)

# MVP
## 迭代思维与 MVP 产品规划方法（OOPD）
![](.README_images/767b46e4.png)

## 如何找出产品的 MVP 功能范围？
![](.README_images/dc35875d.png)

## 企业级数据库设计十个原则
### 基础原则
![](.README_images/9212abf8.png)

### 扩展性原则
![](.README_images/6e3112ec.png)

### 完备性原则
![](.README_images/ba7fb251.png)
