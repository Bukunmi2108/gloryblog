"""User Blog Relationship

Revision ID: e51b98488aac
Revises: 657025bd84c5
Create Date: 2024-10-16 20:32:45.017394

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# revision identifiers, used by Alembic.
revision: str = 'e51b98488aac'
down_revision: Union[str, None] = '657025bd84c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', Column('posts', Integer, ForeignKey('blogs.id')))
    op.execute("""
        ALTER TABLE users
        ADD CONSTRAINT fk_users_posts_blog_posts FOREIGN KEY (posts) REFERENCES blogs(id) ON DELETE CASCADE
    """)

    # Define the relationship in the User model
    User.__mapper__.add_property("posts", relationship("Blog", backref="author", cascade="all, delete-orphan"))


def downgrade() -> None:
    op.drop_column('users', 'posts')
