# kly-quota-api

本 README 提供了如何运行该项目。

## 先决条件
```bash
# 安装依赖
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行项目

```bash
# 项目安装
python3 setup.py install

# 初始化数据库
kly-db-manage revision --autogenerate -m "init_database"
kly-db-manage upgrade head

# 导入数据
kly-db-manage import_data --data-file hardware_data.yml

# 运行项目
kly-quota-api
```
