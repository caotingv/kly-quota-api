import click
import subprocess

from flask import Flask
from kly_quota_api.config import Config
from kly_quota_api.exts import db, migrate
from kly_quota_api.db import hardware
from kly_quota_api.db.models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate.init_app(db=db, app=app)
app_entry_point = "kly_quota_api.db.manage"


@click.group()
def cli():
    """Custom CLI commands for your Flask app."""
    pass


@cli.command()
def db_init():
    """初始化数据库"""

    command = f"flask --app {app_entry_point} db init"
    subprocess.run(command, shell=True, check=True)


@cli.command()
def db_migrate():
    """生成反映模型更改的迁移脚本"""

    command = f"flask --app {app_entry_point} db migrate"
    subprocess.run(command, shell=True, check=True)


@cli.command()
def db_upgrade():
    """更新数据库结构"""

    command = f"flask --app {app_entry_point} db upgrade"
    subprocess.run(command, shell=True, check=True)


@cli.command()
def db_import():
    """导入数据到数据库"""

    with app.app_context():
        try:
            # Adding data to the database session
            for data in hardware.motherboards:
                motherboard = Motherboard(**data)
                db.session.add(motherboard)

            for data in hardware.memorys:
                memory = Memory(**data)
                db.session.add(memory)

            for data in hardware.disks:
                disk = Disk(**data)
                db.session.add(disk)
            # Commit the changes to the database
            db.session.commit()

            print('数据导入成功')
        except Exception as e:
            # Rollback changes and print the error if an exception occurs
            db.session.rollback()
            print('数据导入失败:', str(e))


def main():
    cli()
