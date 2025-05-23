"""Adicionando tabelas de monthly incomes

Revision ID: 497aaa577406
Revises: 9451d6ef8600
Create Date: 2025-04-29 17:15:13.682819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '497aaa577406'
down_revision: Union[str, None] = '9451d6ef8600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monthly_incomes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('net_balance', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('initial_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monthly_incomes_id'), 'monthly_incomes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_monthly_incomes_id'), table_name='monthly_incomes')
    op.drop_table('monthly_incomes')
    # ### end Alembic commands ###
