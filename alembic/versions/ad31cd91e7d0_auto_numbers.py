"""auto numbers

Revision ID: ad31cd91e7d0
Revises: 148ea52c1fc1
Create Date: 2024-10-13 10:20:48.610016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad31cd91e7d0'
down_revision: Union[str, None] = '148ea52c1fc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('categories', 'id')
    op.add_column('categories', sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False))


def downgrade() -> None:
    op.drop_column('categories', 'id')
