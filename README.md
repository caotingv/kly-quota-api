# kly-quota-api

本 README 提供了如何运行该项目。

## 先决条件

在开始之前，请确保已安装以下内容：

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

您还需要在 Flask 应用程序中配置数据库连接。

## 数据库迁移

### 1. 初始化数据库

要初始化数据库（如果尚未创建），请运行以下命令：

```bash
flask db init
```

生成反映模型更改的迁移脚本，请运行以下命令：

```bash
flask db migrate
```

这将在 migrations/versions 目录中创建一个迁移脚本。

要应用迁移并更新数据库结构，请运行以下命令：

```bash
flask db upgrade
```

其他信息

- 确保根据您的 Flask 应用程序的实际情况将 flask-3 替换为正确的命令或脚本。
- 自定义您的模型和数据库配置以适应项目的需求。


## 2. 运行项目

```bash
python3 app.py
```
