"""categories issue

Revision ID: b2d9ab03c188
Revises: 17ed1ea120f8
Create Date: 2024-10-12 22:29:20.770699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d9ab03c188'
down_revision: Union[str, None] = '17ed1ea120f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('categories', sa.Column('id', sa.Integer()))
    op.add_column('categories', sa.Column('tag', sa.String()))


def downgrade() -> None:
    op.drop_column('categories', 'id')
    op.drop_column('categories', 'tag')

