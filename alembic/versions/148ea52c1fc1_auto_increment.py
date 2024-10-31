"""auto increment

Revision ID: 148ea52c1fc1
Revises: 2eac4438dab1
Create Date: 2024-10-13 10:11:16.478962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '148ea52c1fc1'
down_revision: Union[str, None] = '2eac4438dab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('categories', 'id')
    op.add_column('categories', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))


def downgrade() -> None:
    op.drop_column('categories', 'id')
