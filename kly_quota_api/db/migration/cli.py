import os
import yaml

from alembic import command as alembic_cmd
from alembic import config as alembic_cfg
from alembic import util as alembic_u
from oslo_config import cfg
from oslo_db import options
from oslo_log import log

from kly_quota_api.db.models import *

CONF = cfg.CONF
options.set_defaults(CONF)

log.set_defaults()
log.register_options(CONF)
log.setup(CONF, 'kly-db-manage')

def do_alembic_command(config, cmd, *args, **kwargs):
    try:
        getattr(alembic_cmd, cmd)(config, *args, **kwargs)
    except alembic_u.CommandError as e:
        alembic_u.err(str(e))


def do_check_migration(config, _cmd):
    do_alembic_command(config, 'branches')


def add_alembic_subparser(sub, cmd):
    return sub.add_parser(cmd, help=getattr(alembic_cmd, cmd).__doc__)


def do_upgrade(config, cmd):
    if not CONF.command.revision and not CONF.command.delta:
        raise SystemExit(_('You must provide a revision or relative delta'))

    revision = CONF.command.revision or ''
    if '-' in revision:
        raise SystemExit(_('Negative relative revision (downgrade) not '
                           'supported'))

    delta = CONF.command.delta

    if delta:
        if '+' in revision:
            raise SystemExit(_('Use either --delta or relative revision, '
                               'not both'))
        if delta < 0:
            raise SystemExit(_('Negative delta (downgrade) not supported'))
        revision = '%s+%d' % (revision, delta)

    do_alembic_command(config, cmd, revision, sql=CONF.command.sql)


def no_downgrade(config, cmd):
    raise SystemExit(_("Downgrade no longer supported"))


def do_stamp(config, cmd):
    do_alembic_command(config, cmd,
                       CONF.command.revision,
                       sql=CONF.command.sql)


def do_revision(config, cmd):
    do_alembic_command(config, cmd,
                       message=CONF.command.message,
                       autogenerate=CONF.command.autogenerate,
                       sql=CONF.command.sql)

def do_import_data(config, cmd):
    data_file = CONF.command.data_file
    if not data_file:
        raise SystemExit(_('You must provide a data file to import'))
    
    with open(data_file, 'r') as file:
        try:
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)
            if not isinstance(yaml_data, list):
                raise ValueError('YAML data is not a list')

            for item in yaml_data:
                if 'Motherboard' in item:
                    pass
                elif 'Memory' in item:
                    pass
                elif 'Disk' in item:
                    pass
        except yaml.YAMLError as e:
            raise SystemExit(f'Error while parsing YAML file: {e}')
    print(f'Importing data from {data_file}...')
    print('Data imported successfully!')


def add_command_parsers(subparsers):
    for name in ['current', 'history', 'branches']:
        parser = add_alembic_subparser(subparsers, name)
        parser.set_defaults(func=do_alembic_command)

    help_text = (getattr(alembic_cmd, 'branches').__doc__ +
                 ' and validate head file')
    parser = subparsers.add_parser('check_migration', help=help_text)
    parser.set_defaults(func=do_check_migration)

    parser = add_alembic_subparser(subparsers, 'upgrade')
    parser.add_argument('--delta', type=int)
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_upgrade)

    parser = subparsers.add_parser('downgrade', help="(No longer supported)")
    parser.add_argument('None', nargs='?', help="Downgrade not supported")
    parser.set_defaults(func=no_downgrade)

    parser = add_alembic_subparser(subparsers, 'stamp')
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision')
    parser.set_defaults(func=do_stamp)

    parser = add_alembic_subparser(subparsers, 'revision')
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')
    parser.add_argument('--sql', action='store_true')
    parser.set_defaults(func=do_revision)

    parser = subparsers.add_parser('import_data', help="import init data to database")
    parser.add_argument('--data-file', help='Path to the data file to import', required=True)
    parser.set_defaults(func=do_import_data)


command_opt = cfg.SubCommandOpt('command',
                                title='Command',
                                help='Available commands',
                                handler=add_command_parsers)

CONF.register_cli_opt(command_opt)


def main():
    config = alembic_cfg.Config(
        os.path.join(os.path.dirname(__file__), 'alembic.ini')
    )
    config.set_main_option('script_location',
                           'kly_quota_api.db.migration:alembic_migrations')
    # attach the kly-quota-api conf to the Alembic conf
    config.kly_quota_api_config = CONF
    print(CONF.database.connection)
    CONF(project='kly-quota-api')
    CONF.command.func(config, CONF.command.name)

