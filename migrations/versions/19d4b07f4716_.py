"""empty message

Revision ID: 19d4b07f4716
Revises: 490fe81949a6
Create Date: 2023-08-14 17:38:28.760071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19d4b07f4716'
down_revision = '490fe81949a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cpu_motherboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_mem_slot1', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cpu_motherboard', schema=None) as batch_op:
        batch_op.drop_column('max_mem_slot1')

    # ### end Alembic commands ###