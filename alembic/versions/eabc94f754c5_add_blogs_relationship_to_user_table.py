"""Add blogs relationship to User table

Revision ID: eabc94f754c5
Revises: e51b98488aac
Create Date: 2024-10-20 18:25:40.520694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eabc94f754c5'
down_revision: Union[str, None] = 'e51b98488aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Add the blogs relationship to the User table
    op.add_column('users', sa.Column('blogs', sa.Integer()))
    op.execute("ALTER TABLE users ADD FOREIGN KEY (blogs) REFERENCES blogs (id);")

def downgrade():
    # Remove the blogs relationship from the User table
    op.drop_column('user', 'blogs')