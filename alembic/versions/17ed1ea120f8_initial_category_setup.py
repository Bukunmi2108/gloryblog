"""Initial category setup

Revision ID: 17ed1ea120f8
Revises: 
Create Date: 2024-10-12 13:07:26.086206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17ed1ea120f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('categories', sa.Column('id', sa.Integer(), primary_key=True))


def downgrade() -> None:
    op.drop_column('categories', 'id')
