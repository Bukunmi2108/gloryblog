"""Category Foreign key

Revision ID: 99cb7fcaa487
Revises: ad31cd91e7d0
Create Date: 2024-10-13 22:16:48.089970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99cb7fcaa487'
down_revision: Union[str, None] = 'ad31cd91e7d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.drop_column('categories', 'tag')
    op.add_column('categories', sa.Column('tag', sa.Integer(), autoincrement=True, nullable=False))
    op.create_foreign_key(
        "categories_tag_fkey", "categories", "tags", ["tag"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("categories_tag_fkey", "categories", type_=sa.ForeignKey)
    op.drop_column('categories', 'tag')
