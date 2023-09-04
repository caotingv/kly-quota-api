"""empty message

Revision ID: 490fe81949a6
Revises: 
Create Date: 2023-08-14 16:55:39.417585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '490fe81949a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cpu_motherboard',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cpu_model', sa.String(length=32), nullable=False),
    sa.Column('cores', sa.Integer(), nullable=False),
    sa.Column('threads', sa.Integer(), nullable=False),
    sa.Column('frequency', sa.String(length=16), nullable=False),
    sa.Column('max_mem_slot', sa.Integer(), nullable=False),
    sa.Column('max_hard_slot', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpu_model')
    )
    op.create_table('hard',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hard_model', sa.String(length=32), nullable=False),
    sa.Column('interface_type', sa.String(length=16), nullable=False),
    sa.Column('ishdd', sa.Boolean(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hard_model')
    )
    op.create_table('mem',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mem_model', sa.String(length=32), nullable=False),
    sa.Column('mem_frequency', sa.String(length=16), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('mem_type', sa.String(length=8), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mem_model')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mem')
    op.drop_table('hard')
    op.drop_table('cpu_motherboard')
    # ### end Alembic commands ###