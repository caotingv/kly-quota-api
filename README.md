# kly-quota-api

本 README 提供了如何运行该项目。

## 先决条件

在开始之前，请确保已安装以下内容：

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate


## 运行项目

```bash
# 安装
python3 setup.py install

# 初始化数据库
kly-db-manage db-init
kly-db-manage db-migrate
kly-db-manage db-upgrade

# 导入数据
kly-db-manage import-data

# 运行项目
kly-quota-api
```
