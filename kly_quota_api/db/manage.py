import click
import subprocess

from flask import Flask
from kly_quota_api.config import Config
from kly_quota_api.exts import db, migrate
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
def import_data():
    """导入数据到数据库"""

    with app.app_context():
        db.create_all()
        motherboards = [
            {
                "manufacturer": "安擎",
                "cpu_model": "Intel Core i7",
                "cpu_architecture": "x86_64",
                "cpu_threads": 8,
                "cpu_frequency": "3.6 GHz",
                "max_cpu": 2,
                "max_mem": 4,
                "max_sata_hard": 6,
                "max_nvme_hard": 2,
            },
            {
                "manufacturer": "国鑫",
                "cpu_model": "AMD Ryzen 9",
                "cpu_architecture": "x86_64",
                "cpu_threads": 16,
                "cpu_frequency": "3.8 GHz",
                "max_cpu": 2,
                "max_mem": 8,
                "max_sata_hard": 4,
                "max_nvme_hard": 3,
            },
        ]

        try:
            # Adding data to the database session
            for data in motherboards:
                motherboard = Motherboard(**data)
                db.session.add(motherboard)

            # Commit the changes to the database
            db.session.commit()

            print('数据导入成功')
        except Exception as e:
            # Rollback changes and print the error if an exception occurs
            db.session.rollback()
            print('数据导入失败:', str(e))


def main():
    cli()
