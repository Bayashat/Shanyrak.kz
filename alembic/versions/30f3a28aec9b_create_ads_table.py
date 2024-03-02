"""create_ads_table

Revision ID: 30f3a28aec9b
Revises: a9490e91f5e3
Create Date: 2024-03-03 03:00:30.601663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30f3a28aec9b'
down_revision: Union[str, None] = 'a9490e91f5e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('area', sa.Float(), nullable=False),
    sa.Column('rooms_count', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ads_address'), 'ads', ['address'], unique=False)
    op.create_index(op.f('ix_ads_id'), 'ads', ['id'], unique=False)
    op.create_index(op.f('ix_ads_type'), 'ads', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ads_type'), table_name='ads')
    op.drop_index(op.f('ix_ads_id'), table_name='ads')
    op.drop_index(op.f('ix_ads_address'), table_name='ads')
    op.drop_table('ads')
    # ### end Alembic commands ###